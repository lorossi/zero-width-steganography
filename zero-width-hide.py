import os
import logging
import argparse
import zerowidth

def main():
    logging.basicConfig(filename="zero-width-hide.log", level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        filemode="w")

    parser = argparse.ArgumentParser(description="Hide and recover text in plainsight", epilog="You will find a log file with the same name as the script. If any error is raised, check there.")
    parser.add_argument('-V', '--version', help='library version', action='store_true')
    parser.add_argument('-v', '--verbose', help='verbose mode. If activated it will only prompt errors', action='store_true')
    parser.add_argument('-s', '--source', help='source file', type=str)
    parser.add_argument('-d', '--destination', help='destination file - leave empty to output to console', required=False, type=str)
    parser.add_argument('-S', '--sourcetext', help='source text', type=str, required=False)
    parser.add_argument('-E', '--encode', help='encode source', required=False, action="store_true")
    parser.add_argument('-D', '--decode', help='decode source', required=False, action="store_true")
    parser.add_argument('-T', '--text', help='clear text to be encoded string', required=False, type=str)
    parser.add_argument('-t', '--textpath', help='path of a clear text file to be encoded string', required=False, type=str)
    parser.add_argument('-C', '--clean', help='clean source file from hidden text', required=False, action="store_true")
    parser.add_argument('-p', '--position', help='set position of encoded text in destination file. Can be: a list of line numbers, "random", "top", "bottom", "lines", "nth". Defaults to "top"', required=False, default="top")
    parser.add_argument('-l', '--lines', help='set lines of encoded text in destination file if -p parameter is "lines". Defaults to first.', required=False, type=int, nargs="+", default=1)
    parser.add_argument('-o', '--occasions', help='set number of lines of encoded text in destination file if -p parameter is "random", number of lines to skip if -p is "nth". Defaults to 1', required=False, type=int, nargs="+", default=[1])
    args = parser.parse_args()
    z = zerowidth.ZeroWidth()

    if (args.version):
        # the user just wants to know the version
        version = z.version()
        print(f"Zero width version: {version}")
        return

    if not(args.decode or args.encode or args.clean):
        # the user didn't specify what he wants to do
        logging.error("No encode/decode/clean option specified or No destination and encode specified")
        print("No encode/decode/clean option specified or No destination and encode specified")
        parser.print_help()
        return

    if args.decode and not (args.source or args.sourcetext):
        # the user didn't specify a source and is trying to decode
        logging.error("No source file specified")
        print("No source file specified")
        parser.print_help()
        return

    if args.encode and not (args.text or args.textpath):
        # the user didn't specify a source and is trying to encode
        logging.error("No text source\n")
        print("No text source")
        parser.print_help()
        return

    if args.encode and not args.destination:
        # the user didn't specify a destination and is trying to encode
        logging.error("No destination file specified\n")
        print("No destination file specified")
        parser.print_help()
        return

    if args.clean and not args.source:
        # the user didn't specify what file he wants to clean
        logging.error("No text source\n")
        print("No text source")
        parser.print_help()
        return

    if (args.source):
        try:
            # we attempt to read a file source
            z.readFile(args.source)
        except Exception as e:
            logging.error(f"Error while opening source file. Error: {e}")
            print("Couldn't read source file. Look at log for more informations")
            return
        logging.info("Source file loaded")
        if (args.verbose):
            print("Source file loaded")

    elif (args.sourcetext):
        try:
            # we attempt to read console source
            z.readSource(args.sourcetext)
        except Exception as e:
            logging.error(f"Error while reading source text. Error: {e}")
            print("Couldn't read source text. Look at log for more informations")
            return
        logging.info("Source text valid")
        if (args.verbose):
            print("Source text loaded")

    if (args.clean):
        try:
            # we attempt to look for encoded text
            z.searchEncodedText()
            # we attempt to clean it
            z.cleanSource(args.source)
        except Exception as e:
            logging.error(f"Error while cleaning file. Error: {e}")
            print("Couldn't clean file. Look at log for more informations")
            return

        try:
            if args.destination:
                # we write the cleaned file into destination
                z.writeFile(args.destination)
                logging.info("Source file cleaned in destination")
                if (args.verbose):
                    print("Source file cleaned in destination")
                return
            else:
                # we overwrite the current file in order to clear it
                z.writeFile(args.source)
                logging.info("Source file cleaned")
                if (args.verbose):
                    print("Source file cleaned")
                return
        except Exception as e:
                logging.error(f"Error while cleaning file. Error: {e}")
                print("Couldn't clean file. Look at log for more informations")
                return


    elif (args.encode):
        try:
            if args.text:
                # source from console
                cleartext = args.text
            elif args.textpath:
                # source from file
                with open(args.textpath, 'r', encoding='utf-8-sig') as f:
                    cleartext = f.read().splitlines()

        except Exception as e:
            logging.info(f"No clear text found or text couldn't be encoded. Error {e}")
            print("No clear text found or text couldn't be encoded. Look at log for more informations")
            return

        try:
            # we set clear text
            z.setClearText(cleartext)
            # we encode in zero width
            z.zeroEncode()
        except Exception as e:
            logging.info(f"Text couldn't be encoded. Error {e}")
            print("Text couldn't be encoded. Look at log for more informations")
            return

        logging.info("Text encoded")
        if (args.verbose):
            print("Text encoded")

        try:
            if isinstance(args.lines, int):
                # the user has specified only one line
                # we want to wrap it in a list
                args.lines = [args.lines]

            # we embed the text in the source code
            z.embedEncoded(position=args.position, lines=args.lines, occasions=args.occasions)
            # we write the cleaned text into destination
            z.writeFile(args.destination)

        except Exception as e:
            logging.info(f"No clear text found or text couldn't be encoded. Error {e}")
            print("No clear text found or text couldn't be encoded. Look at log for more informations")
            return

        logging.info("Text encoded in output file")
        if (args.verbose):
            print("Text encoded in output file")

        return

    elif (args.decode):
        logging.info("Attempting to decode")
        if (args.verbose):
            print("Attempting to decode"")
        # attempting to decode
        result = z.searchEncodedText()

        if not result:
            logging.info("No encoded text found")
            if (args.verbose):
                print("No encoded text has been found in this file.")
            return

        # number of encoded strings found
        decoded = z.zeroDecode()
        logging.info(f"{len(decoded)} instances of text found")
        # we attempt to decode the encoded text
        decoded_string = z.zeroDecodeString(verbose=args.verbose)

        if (args.destination):
            # if the user has specified a destination file
            try:
                # we write it down
                z.writeFile(args.destination)
                logging.info("Output written to file")
                if (args.verbose):
                    print(f"Output written to file {args.destination}")
                return
            except Exception as e:
                logging.error(f"Error while writing to file. Error: {e}")
                print(f"Couldn't write to file {args.destination}. Look at log for more informations")
                return
        else:
            # otherwise, we print into console
            logging.info("String decoded")
            print(decoded_string)
            return


if __name__ == "__main__":
    main()
