#!/usr/bin/env python3

import argparse

from PhoneticTextCreator import PhoneticTextCreator


def get_parser() -> argparse.ArgumentParser:
    pars = argparse.ArgumentParser(
        description="Replace full text with phonetic description using pronunciation dictionaries")

    pars.add_argument('text',
                      help='text file with text in specific language',
                      type=argparse.FileType('r', encoding='utf-8'),
                      )
    pars.add_argument('wordlist',
                      help='tsv file that stores words and their pronunciationin IPA',
                      type=argparse.FileType('r', encoding='utf-8'),
                      )
    parser.add_argument('--directory', '-d',
                        help='if it is an entire directory that needs to be precessed',
                        action='store_const',
                        const=True)


    return pars


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    print(args.text)

    processor = PhoneticTextCreator(args.wordlist, args.text)

    print(processor.create_phonetic_text())


