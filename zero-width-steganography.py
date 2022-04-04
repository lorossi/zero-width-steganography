import argparse
import zerowidth


def check_args(args: argparse.Namespace) -> bool:
    if args.clear_source and args.file_source:
        print("Invalid options. Pass either a string source or a file source.")
        return False

    if [args.encode, args.decode, args.clean].count(True) != 1:
        print("Invalid options. Pass either encode, decode or clear.")
        return False

    if not (args.clear_source or args.file_source) and args.encode:
        print("Invalid options. Pass one source.")
        return False

    if not args.to_hide and args.encode:
        print("Invalid options. Pass a string to hide.")
        return False

    if args.encode:
        if not args.position:
            args.position = zerowidth.Position.NTHLINES
        else:
            try:
                args.position = zerowidth.Position(int(args.position))
            except ValueError:
                print("Invalid position.")
                return False

        try:
            args.k = int(args.k)
        except ValueError:
            print("Invalid k.")
            return False

    return True


def clean(args: argparse.Namespace):
    z = zerowidth.ZeroWidth()

    if args.file_source:
        cleaned = z.cleanFile(source_path=args.file_source)
    else:
        cleaned = z.clean(source=args.clear_source)

    if args.output_path:
        with open(args.output_path, "w") as f:
            f.write(cleaned)
            return

    print(cleaned)


def encode(args: argparse.Namespace):
    z = zerowidth.ZeroWidth()
    clear = args.to_hide

    if args.file_source:
        encoded = z.zeroEncodeFile(
            source_path=args.file_source, clear=clear, position=args.position, k=args.k
        )
    else:
        encoded = z.zeroEncode(
            clear=clear, source=args.clear_source, position=args.position, k=args.k
        )

    if args.output_path:
        with open(args.output_path, "w") as f:
            f.write(encoded)
            return

    print(encoded)


def decode(args: argparse.Namespace):
    z = zerowidth.ZeroWidth()

    if args.file_source:
        decoded = z.zeroDecodeFile(source_path=args.file_source)
    else:
        decoded = z.zeroDecode(source=args.clear_source)

    if args.output_path:
        with open(args.output_path, "w") as f:
            f.write(decoded)
            return

    print(decoded)


def main():
    parser = argparse.ArgumentParser(
        description="Hide and recover text in plainsight",
    )
    parser.add_argument("-V", "--version", help="library version", action="store_true")
    parser.add_argument("-E", "--encode", help="encode text", action="store_true")
    parser.add_argument("-D", "--decode", help="decode text", action="store_true")
    parser.add_argument("-C", "--clean", help="clear file", action="store_true")
    parser.add_argument("-t", "--to-hide", help="string to encode")
    parser.add_argument("-f", "--file-source", help="file source")
    parser.add_argument("-c", "--clear-source", help="clear string")
    parser.add_argument("-o", "--output-path", help="output path")
    parser.add_argument(
        "-p",
        "--position",
        help="hidden string position. 0 for TOP, 1 for BOTTOM, 2 for RANDOM, "
        "3 for NTHLINES, 4 for RANDOMINLINE",
        default=3,
    )
    parser.add_argument("-k", "-position-k", help="position variator", default=1)

    args = parser.parse_args()

    if not check_args(args):
        return

    if args.version:
        z = zerowidth.ZeroWidth()
        print(f"Zero width version: {z.version}")
        return

    if args.clean:
        clean(args)
        return

    if args.encode:
        encode(args)
        return

    if args.decode:
        decode(args)
        return


if __name__ == "__main__":
    main()
