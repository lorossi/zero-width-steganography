import unittest
from zerowidthspy import ZeroWidth, Position

from random import choices, randint
from string import ascii_letters
from os import remove


def random_str(k=128) -> str:
    return "".join(choices(ascii_letters, k=k))


def random_multiline(n=32, k=128) -> str:
    return "\n".join(random_str(k) for _ in range(n))


TESTS = 100
PATH = "test.log"


class TestSteganography(unittest.TestCase):
    def test_encode_decode(self):
        z = ZeroWidth()

        for _ in range(TESTS):
            k = randint(50, 200)
            s = random_str(k)
            encoded = z._spaceEncode(s)
            decoded = z._spaceDecode(encoded)
            self.assertEqual(s, decoded)

    def test_embed(self):
        z = ZeroWidth()
        for position in Position:
            for _ in range(TESTS):
                num = randint(5, 10)
                clear = random_str(32)
                source = random_multiline(128)
                encoded = z.zeroEncode(
                    source=source, clear=clear, position=position, k=num
                )

                decoded = z.zeroDecode(source=encoded)

                if position in [Position.LINES, Position.NTH, Position.RANDOMINLINE]:
                    self.assertEqual(clear, decoded[: len(clear)])
                else:
                    self.assertEqual(clear, decoded)

                cleaned = z.clean(encoded)
                self.assertEqual(source, cleaned)

    def test_file_encode(self):
        z = ZeroWidth()

        for position in Position:
            for _ in range(TESTS):
                source = random_multiline()
                with open(PATH, "w") as f:
                    f.write(source)

                num = randint(5, 10)
                clear = random_str(k=32)
                encoded = z.zeroEncodeFile(
                    source_path=PATH, clear=clear, position=position, num=num
                )

                with open(PATH, "w") as f:
                    f.write(encoded)

                decoded = z.zeroDecodeFile(source_path=PATH)

                if position in [Position.LINES, Position.NTH, Position.RANDOMINLINE]:
                    self.assertEqual(clear, decoded[: len(clear)])
                else:
                    self.assertEqual(clear, decoded)

        remove(PATH)

    def test_edge_cases(self):
        z = ZeroWidth()

        # empty encoded string
        clear = ""
        source = random_multiline(128)
        encoded = z.zeroEncode(source=source, clear=clear, position=Position.LINES)
        decoded = z.zeroDecode(source=encoded)
        self.assertEqual(clear, decoded[: len(clear)])

        # single line string
        clear = random_str()
        source = random_multiline(128)
        encoded = z.zeroEncode(source=source, clear=clear, position=Position.LINES)
        decoded = z.zeroDecode(source=encoded)
        self.assertEqual(clear, decoded[: len(clear)])


if __name__ == "__main__":
    unittest.main()
