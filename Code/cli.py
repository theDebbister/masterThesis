#!/usr/bin/env python3

import argparse

from PhoneticTextCreator import PhoneticTextCreator


def get_parser() -> argparse.ArgumentParser:
    pars = argparse.ArgumentParser(
        description="Replace full text with phonetic description using pronunciation dictionaries")

    pars.add_argument('text',
                      help='Text(s) that need to be converted into phonetic texts. '
                           'Either txt file or csv containing paths.'
                           'Csv must be first text path, then wordlist path.',
                      )
    pars.add_argument('--wordlist', '-wl',
                      help='tsv file that stores words and their pronunciation in IPA',
                      required=False,
                      )

    pars.add_argument('--csv',
                      help='If it is a csv file containing paths to both text and wordlist',
                      action='store_const',
                      const=True,
                      default=False)

    return pars


def validate_args(arguments: argparse.Namespace) -> dict:
    args_dict = {
        arg: value for arg, value in vars(arguments).items()
        if value is not None
    }

    # args csv and wl are mutually exclusive
    if args_dict["csv"] == ("wordlist" in args_dict):
        print("You can either combine text and wordlist or specify that it is an csv file that needs to be processed.")
        exit(1)

    return args_dict


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    valid_args = validate_args(args)

    processor = PhoneticTextCreator(**valid_args)

    processor.create_csv()

