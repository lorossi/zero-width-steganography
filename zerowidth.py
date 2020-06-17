from random import randint

class ZeroWidth():
    def __init__(self):
        self.text_clear = []
        self.text_encoded = []
        self.raw = ""
        self.character_map = {
            "0" : u'\u200B', # ZERO WIDTH SPACE
            "1" : u'\uFEFF' # ZERO WIDTH NO-BREAK SPACE
        }
        self.space_map = {v: k for k, v in self.character_map.items()}

    def setClearText(self, text_clear):
        if isinstance(text_clear, str):
            new_dict = {"text" : text_clear}
            self.text_clear.append(new_dict)
        else:
            for t in text_clear:
                new_dict = {"text" : t}
                self.text_clear.append(new_dict)

    def setEncodedText(self, text_encoded):
        if not text_encoded.endswith("\n"):
            text_encoded += "\n"
        self.text_encoded = [{"text" : text_encoded, "line" : 1}]

    def searchEncodedText(self):
        self.text_encoded = []
        linecount = 1

        for line in self.raw.splitlines():
            new_dict = {}
            new_dict["text"] = ""
            for c in line:
                if c in list(self.space_map.keys()):
                    new_dict["text"] += c

            if len(new_dict["text"]) % 9 == 0 and new_dict["text"]:
                new_dict["line"] = linecount
                self.text_encoded.append(new_dict)
            linecount += 1

        if len(self.text_encoded) > 0:
            return True
        return False

    def zeroEncode(self):
        for text in self.text_clear:
            self.raw_bits = "".join(format(ord(c), '09b') for c in text["text"])
            self.bits = ""
            for r in self.raw_bits:
                if ord(r) != 65279:
                    self.bits += r
            new_dict = {}
            new_dict["text"] = "".join(self.character_map[b] for b in self.bits)
            self.text_encoded.append(new_dict)

        all_dict = {"all" : "".join(t["text"] for t in self.text_encoded)}
        self.text_encoded.append(all_dict)
        return self.text_encoded

    def zeroDecode(self):
        self.text_clear = []
        for text in self.text_encoded:
            new_dict = {}
            self.decoded = "".join(self.space_map[s] for s in text["text"])
            new_dict["text"] = ""

            for x in range(0, len(self.decoded), 9):
                current_char = self.decoded[x:x+9]
                new_dict["text"] += chr(int(current_char, base=2))

            new_dict["text"] = new_dict["text"].rstrip()
            new_dict["line"] = text["line"]
            self.text_clear.append(new_dict)
        return self.text_clear

    def zeroDecodeString(self):
        self.decoded_string = ""
        for dict in self.text_clear:
            newl = "\n"
            tab = "\t"
            output = (
                f"Text found in line {dict['line']}:"
                f"{tab}{dict['text'].replace(newl, ' ')}{newl}"
            )
            self.decoded_string += output

        self.decoded_string = self.decoded_string.rstrip()
        self.output_buffer = self.decoded_string
        return self.decoded_string

    def readFile(self, path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            self.raw = f.read()

    def writeFile(self, path):
        with open(path, 'w',  encoding='utf-8-sig') as f:
            f.write(self.output_buffer)

    def emdedEncoded(self, position="top", lines=None, occasions=1):
        self.lines = self.raw.splitlines()
        if self.lines == []:
            self.lines = [""]

        if position == "lines":
            linecount = 0
            for p in lines:
                index = linecount % (len(self.text_encoded) - 1)
                self.lines[p-1] += self.text_encoded[index]["text"]
                linecount += 1

        elif position == "nth":
            for i in range(1, len(self.lines) - 1, occasions):
                index = (i - 1) % (len(self.text_encoded) - 1)
                self.lines[i-1] += self.text_encoded[index]["text"]

        elif position == "top":
            self.lines[0] += self.text_encoded[-1]["all"]

        elif position == "bottom":
            self.lines[-1] = self.text_encoded[-1]["all"] + self.lines[-1]

        elif position == "lines":
            linecount = 0
            for x in range(0, len(self.lines), occasions):
                index = linecount % (len(self.text_encoded) - 1)
                self.lines[x] += self.text_encoded[index]["text"]
                linecount += 1

        elif position == "random":
            for x in range(occasions):
                found = False

                while not found:
                    if len(self.lines) == 1:
                        random_line = 0
                    else:
                        random_line = randint(0, len(self.lines) - 1)
                        print("generated")

                    if len(self.lines[random_line]) < 3:
                        found = False
                        continue

                    random_pos = randint(1, len(self.lines[random_line]) - 2)
                    current_line = self.lines[random_line]

                    if current_line[random_pos - 1] in self.space_map.keys() or current_line[random_pos + 1] in self.space_map.keys():
                        found = False
                    else:
                        found = True

                random_encoded = randint(0, len(self.text_encoded))
                self.lines[random_line] = self.lines[random_line][:random_pos] + self.text_encoded[random_encoded]["text"] + self.lines[random_line][random_pos:]

        self.output_buffer = "".join(line + '\n' for line in self.lines)
        return len(self.lines)

    def cleanFile(self, path):
        if self.text_encoded == []:
            self.output_buffer =  self.raw
            return

        else:
            lines = self.raw.splitlines()

            for text in self.text_encoded:
                lines[text["line"] - 1] = lines[text["line"] - 1].replace(text["text"], "")

        self.output_buffer = "".join(line + '\n' for line in lines)

        return len(lines)
