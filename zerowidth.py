"""Class handling the Steganography."""

from random import randint
from enum import Enum


class Position(Enum):
    """
    Enum class handling the positioning of the hidden text.

        TOP: Before the first line of the text
        BOTTOM: After the first line of the text
        RANDOM: In a random line in the text
        NTHLINES: At the end of every nth-line, as specified by the parameter k
        RANDOMINLINE: In every line at a random position
    """

    TOP = 0
    BOTTOM = 1
    RANDOM = 2
    NTHLINES = 3
    RANDOMINLINE = 4


class ZeroWidth:
    """Class handling the steganography embedding in files and strings."""

    def __init__(self) -> None:
        """Initialize a ZeroWidth instance."""
        self._version = "1.1"
        # maps bits to spaces
        self._character_map = {
            "0": "\u200B",  # ZERO WIDTH SPACE
            "1": "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE
        }

        # reverses the "character_map" dict so we can map spaces to bits
        self._space_map = {v: k for k, v in self._character_map.items()}
        # get the special hidden characters
        self._hidden_characters = set(self._space_map.keys())

    def _spaceEncode(self, clear: str) -> str:
        """Encode the string into spaces.

        Args:
            clear (str): clear string to encode

        Returns:
            str
        """
        if len(clear) == 0:
            return ""

        binary = "".join(format(ord(c), "08b") for c in clear)
        return "".join(self._character_map[b] for b in binary)

    def _spaceDecode(self, encoded: str) -> str:
        """Decode the string from spaces.

        Args:
            encoded (str): encoded string

        Returns:
            str
        """
        if len(encoded) == 0:
            return ""

        binary = "".join(self._space_map[e] for e in encoded)
        decoded = "".join(
            chr(int(binary[x : x + 8], 2)) for x in range(0, len(encoded), 8)
        )

        return decoded

    def zeroEncode(
        self, source: str, clear: str, position: Position, k: int = 1
    ) -> str:
        """Encode clear string and hides into the source string in position according \
        to the parameter.

        Args:
            source (str): text that will contain the hidden strings
            clear (str): string to hide in the text
            position (Position): position of the hidden strings.
            k (int, optional): specifies:
                The occurrences of the encoded string in the clear text if Position is Random.
                The number of clear lines between hidden lines if Position is NTHLINE.
            Defaults to 1.

        Returns:
            str: string containing the encoded text
        """
        encoded = self._spaceEncode(clear)

        match position:
            case position.TOP:
                embedded = encoded + source
            case position.BOTTOM:
                embedded = source + encoded
            case position.RANDOM:
                count = 0
                while count < k:
                    k = randint(0, len(source) - 1)
                    if source[k] in self._hidden_characters:
                        continue
                    embedded = source[:k] + encoded + source[k:]
                    count += 1
            case position.NTHLINES:
                lines = source.split("\n")
                for x in range(0, len(lines), k):
                    lines[x] += encoded
                embedded = "\n".join(lines)
            case position.RANDOMINLINE:
                lines = source.split("\n")
                for x in range(0, len(lines), k):
                    k = randint(0, len(lines[x]) - 1)
                    lines[x] = lines[x][:k] + encoded + lines[x][k:]
                embedded = "\n".join(lines)

        return embedded

    def zeroDecode(self, source: str) -> str:
        """Decode an hidden string.

        Args:
            source (str): text containing hidden strings

        Returns:
            str
        """
        encoded = "".join(s for s in source if s in self._hidden_characters)
        return self._spaceDecode(encoded)

    def zeroEncodeFile(
        self, source_path: str, clear: str, position: Position, k: int = 1
    ) -> None:
        """Encode string using a file for source.

        Args:
            source_path (str): path of source file
            clear (str): string to hide in the text
            position (Position): position of the hidden strings.
            k (int, optional): specifies:
                The occurrences of the encoded string in the clear text if Position is Random.
                The number of clear lines between hidden lines if Position is NTHLINE.
            Defaults to 1.
        """
        with open(source_path, "r") as f:
            source = f.read()

        return self.zeroEncode(source=source, clear=clear, position=position, k=k)

    def zeroDecodeFile(self, source_path: str) -> str:
        """Decode an hidden string in a file.

        Args:
            source_path (str): path of the file containing the hidden string

        Returns:
            str: decoded string
        """
        with open(source_path, "r") as f:
            source = f.read()

        return self.zeroDecode(source)

    def cleanString(self, source: str) -> str:
        """Clean a string from hidden characters.

        Args:
            source (str): string containing hidden characters

        Returns:
            str
        """
        return "".join(s for s in source if s not in self._hidden_characters)

    def cleanFile(self, source_path: str) -> str:
        """Clean a string from hidden characters, using a file as source.

        Args:
            source_path (str): path of the file

        Returns:
            str
        """
        with open(source_path, "r") as f:
            source = f.read()

        return self.cleanString(source)

    @property
    def version(self) -> str:
        """Return current version.

        Returns:
            str
        """
        return self._version
