# zerowidthspy -> Zero Width Steganography Python

from random import randint
from enum import Enum


class Position(Enum):
    TOP = 0
    BOTTOM = 1
    RANDOM = 2
    LINES = 3
    NTH = 4
    RANDOMINLINE = 5


class ZeroWidth:
    def __init__(self):
        self._version = "1.0"
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
        if len(clear) == 0:
            return ""

        binary = "".join(format(ord(c), "08b") for c in clear)
        return "".join(self._character_map[b] for b in binary)

    def _spaceDecode(self, encoded: str) -> str:
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
            case position.LINES:
                embedded = source.replace("\n", f"{encoded}\n")
            case position.NTH:
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
        encoded = "".join(s for s in source if s in self._hidden_characters)
        return self._spaceDecode(encoded)

    def zeroEncodeFile(
        self, source_path: str, clear: str, position: Position, num: int = 1
    ) -> None:
        with open(source_path, "r") as f:
            source = f.read()

        return self.zeroEncode(source=source, clear=clear, position=position, k=num)

    def zeroDecodeFile(self, source_path: str) -> str:
        with open(source_path, "r") as f:
            source = f.read()

        return self.zeroDecode(source)

    def clean(self, source: str) -> str:
        return "".join(s for s in source if s not in self._hidden_characters)
