#!/usr/bin/env python3

import argparse

from PhoneticTextCreator import PhoneticTextCreator


def get_parser() -> argparse.ArgumentParser:
    pars = argparse.ArgumentParser(
        description="Replace full text with phonetic description using pronunciation dictionaries")

    pars.add_argument('text',
                      help='Text(s) that need to be converted into phonetic texts. '
                           'Either txt file or csv containing paths.'
                           'Csv must look like this: lang-code, path-original, path-wordlist',
                      )
    pars.add_argument('--wordlist', '-wl',
                      help='tsv file that stores words and their pronunciation in IPA',
                      required=False,
                      )

    pars.add_argument('--name', '-n',
                      help="in case you'd like to create several version of the same texts using different settings, "
                           "you can add version names here",
                      type=str,
                      )

    pars.add_argument('--concat', '-c',
                      help="If this option is chosen, words that are not in the wordlists will be split iteratively "
                           "and concatenated if word parts are in the list",
                      action='store_const',
                      const=True,
                      default=False,
                      )

    pars.add_argument('--language', '-l',
                      help='Only necessary if a single text and a wordlist is passed',
                      type=str,
                      )

    return pars


def validate_args(arguments: argparse.Namespace) -> dict:
    args_dict = {
        arg: value for arg, value in vars(arguments).items()
        if value is not None
    }

    # args csv and wl are mutually exclusive
    if ("language" in args_dict) != ("wordlist" in args_dict):
        print("You need to pass both wordlist and language or a csv only.")
        exit(1)

    return args_dict


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    valid_args = validate_args(args)

    processor = PhoneticTextCreator(**valid_args)

