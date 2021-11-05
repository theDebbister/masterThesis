import os
from segments import Profile
import argparse
import pandas as pd
import re

# example: get global phoneme cluster counts for JIPA stories
# python lang_profiles_stats.py lang_profiles_JIPA_SIG\ --dir --cluster



def get_parser():
    parser = argparse.ArgumentParser(description='Get different statistics of grapheme-to-phoneme data.')

    parser.add_argument('inpath',
                        help='Either tsv profile file [Grapheme, mapping, frequency] or dir, if dir specify by adding --dir')
    parser.add_argument('--output_dir', '-o',
                        help='Name of dir for output',
                        type=str)
    parser.add_argument('--directory', '-d',
                        action='store_true',
                        help='Specifies if the input is a directory with files',
                        )
    parser.add_argument('--cluster',
                        action='store_true',
                        help='Specifies the counts for the phoneme clusters should be calculated or for the phonemes',
                        )

    return parser


def get_global_counts(path: str, directory=False, cluster=False, output_dir=''):

    character_list = []

    if directory:
        character_list += __get_chars_from_profile_dir(path, cluster)

    else:
        character_list = __get_chars_from_profile_file(path)

    phoible = pd.read_csv('phoible.csv')
    phons = set(phoible['Phoneme'])
    all_chars = set(character_list)
    intersection = phons.intersection(all_chars)
    difference = all_chars.difference(intersection)

    if cluster:
        with open(output_dir + 'phon_clusters_not_in_phoible.txt' if output_dir else 'phon_clusters_not_in_phoible.txt',
                  'w', encoding='utf8') as out_clusters:
            for p in difference:
                out_clusters.write(p + '\n')
    else:
        with open(output_dir + 'phons_not_in_phoible.txt' if output_dir else 'phons_not_in_phoible.txt',
                  'w', encoding='utf8') as out_phon:
            for p in difference:
                out_phon.write(p + '\n')

    print(f'Num phons phoible: {len(phons)}')
    print(f'Num phons profiles: {len(all_chars)}')
    print(f'Num phons intersection: {len(intersection)}')
    print(f'Num phons only in profiles: {len(difference)}')


def __get_chars_from_profile_file(filename: str) -> list:
    tsv = pd.read_csv(filename, sep='\t', index_col=False)
    return [g.strip() for g in tsv['Grapheme'].to_list()]


def __get_chars_from_profile_dir(directory: str, cluster=False) -> list:
    chars = []
    for filename in os.listdir(directory):
        if cluster:
            if 'phon' in filename and 'clusters' in filename:
                print(filename)
                chars.extend(__get_chars_from_profile_file(directory + '/' + filename))

        else:
            if 'phon' in filename and 'clusters' not in filename:
                print(filename)
                chars.extend(__get_chars_from_profile_file(directory + '/' + filename))

    return chars


# def get_stats(profile1, profile2):
#     prf1 = Profile.from_file(profile1)
#     prf2 = Profile.from_file(profile2)
#
#     l1 = [p for p in prf1.iteritems()]
#     l2 = [p for p in prf2.iteritems()]
#
#     intersect = [x['Grapheme'] for x in l1 if x['Grapheme'] in [y['Grapheme'] for y in l2]]
#
#     l1_only = [x['Grapheme'] for x in l1 if x['Grapheme'] not in intersect]
#     l2_only = [x['Grapheme'] for x in l2 if x['Grapheme'] not in intersect]
#
#     percentage_l1_in_l2 = (len(intersect) / len(l1)) * 100
#     percentage_l2_not_in_l1 = (len(l2_only) / len(l2)) * 100
#
#     print(f'Intersection of profile 1 and profile 2: {intersect}')
#     print(f'Percentage of characters profile 1 (train) that is covered in profile 2 (test): {round(percentage_l1_in_l2, 2)}%')
#     print(f'Percentage of characters profile 2 (test) that is not in profile 1 (train): {round(percentage_l2_not_in_l1, 2)}%')


def get_statistics(inpath, directory=False, output_dir='', cluster=False):
    get_global_counts(inpath, directory=directory, cluster=cluster, output_dir=output_dir)


if __name__ == '__main__':
    p = get_parser()
    args = p.parse_args()

    print(args)

    get_statistics(**vars(args))


