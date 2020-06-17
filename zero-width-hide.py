import logging
import argparse
import zerowidth

def main():
    logging.basicConfig(filename="zero-width-hide.log", level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode="w")

    parser = argparse.ArgumentParser(description="Hide and recover text in plainsight", epilog="\n")

    parser.add_argument('-s', '--source', help='source file', type=str)
    parser.add_argument('-d', '--destination', help='destination file - leave empty to output to console', required=False, type=str)
    parser.add_argument('-E', '--encode', help='encode source', required=False, action="store_true")
    parser.add_argument('-D', '--decode', help='decode source', required=False, action="store_true")
    parser.add_argument('-t', '--text', help='clear text to be encoded string (or filepath - TODO)', required=False, type=str)
    parser.add_argument('-C', '--clean', help='clean source file from hidden text', required=False, action="store_true")
    parser.add_argument('-p', '--position', help='set position of encoded text in destination file. Can be: a list of line numbers, "random", "top", "bottom", "lines". Defaults to "top"', required=False)
    parser.add_argument('-l', '--lines', help='set lines of encoded text in destination file if -p parameter is "lines". Defaults to 1', required=False, type=int, nargs="+")
    parser.add_argument('-o', '--occasions', help='set number of lines of encoded text in destination file if -p parameter is "lines", defaults to 1', required=False, type=int, nargs="+")
    args = parser.parse_args()

    if not(args.decode or args.encode or args.clean):
        parser.print_help()
        logging.error("No encode/decode/clean option specified or No destination and encode specified")
        return

    if args.decode and not args.source:
        parser.print_help()
        logging.error("No source file specified")

    if args.encode and not args.text:
        parser.print_help()
        logging.error("No text source")

    if args.clean and not args.source:
        parser.print_help()
        logging.error("No text source")

    z = zerowidth.ZeroWidth()

    if (args.source):
        try:
            z.readFile(args.source)
        except Exception as e:
            logging.error(f"Error while opening file. Error: {e}")
            print("Couldn't read file")
            return
        logging.info("File loaded")


    if (args.clean):
        try:
            z.searchEncodedText()
            z.cleanFile(args.source)
        except Exception as e:
            logging.error(f"Error while cleaning file. Error: {e}")
            print("Couldn't clean file")
            return
        logging.info("File cleaned")
        print("File cleaned")
        return


    elif (args.encode):
        try:
            z.setClearText(args.text)
            z.zeroEncode()
        except Exception as e:
            logging.info(f"No clear text found or text coulnd't be encoded. Error {e}")
            print("No clear text found or text coulnd't be encoded")
            return

        logging.info("Text encoded")

        try:
            if args.source:
                z.readFile(args.source)
            if args.position and args.lines:
                z.emdedEncoded(args.position, args.lines)
            elif args.position:
                 z.emdedEncoded(args.position, [1])
            else:
                z.emdedEncoded()
            z.writeFileEncoded(args.destination)

        except Exception as e:
            logging.info(f"No clear text found or text coulnd't be encoded. Error {e}")
            print("No clear text found or text coulnd't be encoded")
            return

        logging.info("Text encoded in output file")
        print("Text encoded in output file")

        return

    elif (args.decode):
        logging.info("Attempting to decode")
        result = z.searchEncodedText()

        if not result:
            logging.info("No encoded text found")
            print("No encoded text has been found in this file")
            return

        decoded = z.zeroDecode()
        logging.info(f"{len(decoded)} instances of text found")

        decoded_string = z.zeroDecodeString()

        if (args.destination):
            try:
                z.writeFileDecoded(args.destination)
                logging.info("Output written to file")
                print(f"Output written to file {args.destination}")
                return
            except Exception as e:
                logging.error(f"Error while writing to file. Error: {e}")
                print(f"Couldn't write to file {args.destination}")
                return
        else:
            logging.info("String decoded")
            print(decoded_string)
            return


if __name__ == "__main__":
    main()
