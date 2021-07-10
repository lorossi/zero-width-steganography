# zerowidthspy -> Zero Width Steganography Python

from random import randint, choice


class ZeroWidth():
    def __init__(self):
        self.version_string = "1.0"
        self.clear_text = []
        self.text_encoded = []
        self.raw = ""
        # maps bits to spaces
        self.character_map = {
            "0": u'\u200B',  # ZERO WIDTH SPACE
            "1": u'\uFEFF'  # ZERO WIDTH NO-BREAK SPACE
        }

        # reverses the "character_map" dict so we can map spaces to bits
        self.space_map = {v: k for k, v in self.character_map.items()}
        # get the special hidden characters
        self.hidden_characters = list(self.space_map.keys())

    def setClearText(self, clear_text):
        # THESE ARE THE STRINGS THAT WILL BE HIDDEN
        # clear_text can be both string or list. We want to differentiate
        if isinstance(clear_text, str):
            # passed text is a string
            new_dict = {"text": clear_text}
            self.clear_text.append(new_dict)
        elif isinstance(clear_text, list):
            # passed text is a list
            for t in clear_text:
                new_dict = {"text": t}
                self.clear_text.append(new_dict)
        else:
            # try to stringify it
            new_dict = {"text": str(clear_text)}
            self.clear_text.append(new_dict)

        # clear_text is now list of dicts, each of one has a "text" field
        #   containing the clear text

    def setEncodedText(self, text_encoded):
        # THIS IS THE STRING THAT WILL BE DECODED
        if not text_encoded.endswith("\n"):
            # add newline character
            text_encoded += "\n"
        self.text_encoded = [{"text": text_encoded, "line": 1}]
        # text_encoded is now a list of dicts
        # should probably make multiple dicts?
        #   don't really know why it's a single dict

    def searchEncodedText(self):
        # search for encoded text in source
        self.text_encoded = []
        linecount = 1

        for line in self.raw.splitlines():
            new_dict = {}
            new_dict["text"] = ""
            for c in line:
                # check if the character is in the
                if c in self.hidden_characters:
                    new_dict["text"] += c

            # check if we found a multiple of 9 "bits" (a char)
            if len(new_dict["text"]) % 9 == 0 and new_dict["text"]:
                new_dict["line"] = linecount
                self.text_encoded.append(new_dict)
            linecount += 1

        if len(self.text_encoded) > 0:
            return True
        return False

    def zeroEncode(self):
        # encodes the text into zero width text
        self.text_encoded = []

        for text in self.clear_text:
            # we read the chars and convert it to bits
            self.raw_bits = "".join(format(ord(c), '09b')
                                    for c in text["text"])
            self.bits = ""
            for r in self.raw_bits:
                if ord(r) != 65279:  # BOM mark
                    self.bits += r
            new_dict = {}
            new_dict["text"] = "".join(self.character_map[b]
                                       for b in self.bits)
            self.text_encoded.append(new_dict)

        # the last dict of the list contains all encoded text
        # in a single string
        all_dict = {"all": "".join(t["text"] for t in self.text_encoded)}
        self.text_encoded.append(all_dict)
        return self.text_encoded

    def zeroDecode(self):
        # decodes the text into utf-8
        self.clear_text = []
        for text in self.text_encoded:
            new_dict = {}
            self.decoded = "".join(self.space_map[s] for s in text["text"])
            new_dict["text"] = ""

            for x in range(0, len(self.decoded), 9):
                current_char = self.decoded[x:x+9]
                new_dict["text"] += chr(int(current_char, base=2))

            new_dict["text"] = new_dict["text"].rstrip()
            new_dict["line"] = text["line"]
            self.clear_text.append(new_dict)
        return self.clear_text

    def zeroDecodeString(self, **kwargs):
        # creates string from decoded text
        spacing = " --- "
        self.decoded_string = ""

        if kwargs["verbose"]:
            # verbose mode: more informations
            self.decoded_string += (
                f"{len(self.clear_text)} instances "
                f"of hidden text found \n"
            )
            for dict in self.clear_text:
                output = (
                    f"Text found in line {dict['line']}:\n"
                    f"\t{dict['text'].replace('\n', ' ')}\n"
                )
                self.decoded_string += output
        else:
            # non verbose mode: less informations
            for dict in self.clear_text:
                output = (
                    f"{dict['line']}{spacing}"
                    f"{dict['text'].replace('\n', ' ')} \n"
                )
                self.decoded_string += output

        self.decoded_string = self.decoded_string.rstrip()
        self.output_buffer = self.decoded_string
        return self.decoded_string

    def readSource(self, source):
        # reads from direct input
        self.raw = source

    def readFile(self, path):
        # reads from file
        with open(path, 'r', encoding='utf-8-sig') as f:
            self.raw = f.read()

    def writeFile(self, path):
        # writes to file
        with open(path, 'w',  encoding='utf-8-sig') as f:
            f.write(self.output_buffer)

    # kwargs:
    #   position = lines|nth|top|bottom|random
    #   occasions = (int)
    #   lines = (int)
    def embedEncoded(self, **kwargs):
        self.lines = self.raw.splitlines()
        if self.lines == []:
            # we only found one empty line
            self.lines = [""]

        # hides in every line (or in a list of lines)
        if kwargs["position"] == "lines":
            linecount = 0
            for linecount, p in enumerate(kwargs["lines"]):
                index = linecount % (len(self.text_encoded) - 1)
                self.lines[p-1] += self.text_encoded[index]["text"]

        # hides text every nth lines
        elif kwargs["position"] == "nth":
            textcount = 0
            for i in range(1, len(self.lines) - 1, kwargs["occasions"][0]):
                self.lines[i-1] += self.text_encoded[textcount]["text"]
                textcount = (textcount + 1) % (len(self.text_encoded) - 1)

        # hides at top of document
        elif kwargs["position"] == "top":
            self.lines[0] += self.text_encoded[-1]["all"]

        # hides at bottom of document
        elif kwargs["position"] == "bottom":
            self.lines[-1] = self.text_encoded[-1]["all"] + self.lines[-1]

        # hides at random positions inside document
        elif kwargs["position"] == "random":

            if kwargs["occasions"][0] > len(self.lines):
                # there are more occasions than lines
                raise Exception(
                    "There can't be more occasions than lines. Aborting")

            if kwargs["occasions"][0] < len(self.text_encoded) - 2:
                # there are more lines of text to be encoded
                # than lines in document
                raise Exception(
                    "There can't be less occasions than lines of "
                    "text to be encoded. Aborting")

            # list of free lines (as opposing to brute-forcing every line)
            available_lines = []
            for i in range(0, len(self.lines) - 1):
                if len(self.lines[i]) > 2:
                    available_lines.append(i)

            if len(available_lines) < kwargs["occasions"][0]:
                # the lines are too short to hide text
                raise Exception(
                    "There are not enough available lines in the source file. "
                    "Every line available should be at least "
                    "2 characters wide. Aborting."
                )

            current_encoded = 0
            for _ in range(kwargs["occasions"][0]):

                # pick a random line
                line = choice(available_lines)
                available_lines.remove(line)
                current_line = self.lines[line]

                # try to fit the text inside said line
                #   (not as first or last character)
                found = False
                while not found:
                    pos = randint(1, len(current_line) - 2)
                    prev = current_line[pos - 1]
                    next = current_line[pos + 1]
                    if [prev, next] in self.space_map.keys():
                        # neighbouring characters must not be already hidden
                        found = False
                    else:
                        found = True

                # insert the encoded text in line
                self.lines[line] = self.lines[line][:pos] \
                    + self.text_encoded[current_encoded]["text"] \
                    + self.lines[line][pos:]
                # rotate to next text
                current_encoded = (current_encoded +
                                   1) % (len(self.text_encoded) - 1)

        # text is now ready to be written
        self.output_buffer = "".join(line + '\n' for line in self.lines)
        return len(self.lines)

    def cleanSource(self, path):
        # remove everything from source
        if self.text_encoded == []:
            self.output_buffer = self.raw
            return

        else:
            lines = self.raw.splitlines()

            # this way we preserve any zero-width character
            # inside the text document
            for text in self.text_encoded:
                lines[text["line"] - 1] = lines[text["line"] -
                                                1].replace(text["text"], "")

        self.output_buffer = "".join(line + '\n' for line in lines)

        return len(lines)

    # property getter
    @property
    def version(self):
        # return the version of the library
        return self.version_string
