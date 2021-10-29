import os
from segments import Profile
import argparse
import pandas as pd


def get_parser():
    parser = argparse.ArgumentParser(description='Get different statistics of grapheme-to-phoneme data.')

    parser.add_argument('input',
                        help='Either tsv file [Grapheme, mapping, frequency] or dir, if dir specify by adding --dir')
    parser.add_argument('--output_dir', '-o',
                        help='Name of dir where output is directed to')
    parser.add_argument('--compare', '-c',
                        required=False,
                        help='Either tsv file [Grapheme, mapping, frequency] or dir, if dir specify by adding --dir. '
                             'If this is specified it will '
                             'be used to compare to the first input argument file(s)')
    parser.add_argument('--global',
                        help='Collect global counts. If there is a compare file/dir, both will be '
                             'calculated separately and compared.')
    parser.add_argument('--dir',
                        action='store_true',
                        help='Specifies if the input is a directory with files',
                        )

    return parser


def get_global_counts(path: str, compare='', directory=False):

    if directory:
        character_set = __get_chars_from_profile_dir(path)
        if compare:
            character_set_compare = __get_chars_from_profile_dir(compare)

    else:
        character_set = __get_chars_from_profile_file(path)
        if compare:
            character_set_compare = __get_chars_from_profile_file(compare)


def __get_chars_from_profile_file(filename: str) -> list:
    tsv = pd.read_csv(filename, sep='\t')
    return tsv['Graphemes'].to_list()


def __get_chars_from_profile_dir(directory: str) -> list:
    chars = []
    for filename in os.listdir(directory):
        chars.extend(__get_chars_from_profile_file(filename))

    return chars


def get_stats(profile1, profile2):
    prf1 = Profile.from_file(profile1)
    prf2 = Profile.from_file(profile2)

    l1 = [p for p in prf1.iteritems()]
    l2 = [p for p in prf2.iteritems()]

    intersect = [x['Grapheme'] for x in l1 if x['Grapheme'] in [y['Grapheme'] for y in l2]]

    l1_only = [x['Grapheme'] for x in l1 if x['Grapheme'] not in intersect]
    l2_only = [x['Grapheme'] for x in l2 if x['Grapheme'] not in intersect]

    percentage_l1_in_l2 = (len(intersect) / len(l1)) * 100
    percentage_l2_not_in_l1 = (len(l2_only) / len(l2)) * 100

    print(f'Intersection of profile 1 and profile 2: {intersect}')
    print(f'Percentage of characters profile 1 (train) that is covered in profile 2 (test): {round(percentage_l1_in_l2, 2)}%')
    print(f'Percentage of characters profile 2 (test) that is not in profile 1 (train): {round(percentage_l2_not_in_l1, 2)}%')


if __name__ == '__main__':
    p = get_parser()
    args = p.parse_args()


