import sys
import os
import pandas as pd
from segments import Profile
from segments import Tokenizer
from collections import Counter
import re
import unicodedata


# example:
# python create_lang_profiles_from_g2p_dict.py wikipron_100LC\high\ mock_files\


def wikipron_to_lang_profiles(directory: str, output_directory: str):
    for filename in os.listdir(directory):
        name = filename[:-4].strip('.')
        tsv = pd.read_csv(directory + '/' + filename, delimiter='\t', names=['graphemes', 'phonemes'],
                          dtype={'graphemes': str, 'phonemes': str}, na_filter=False)

        # convert phon / graph lists to string, each word separated by newline, as chars are separated by space
        phonemes = '\n'.join(tsv['phonemes'].to_list())
        graphemes = '\n'.join(tsv['graphemes'].to_list())

        profile_grapheme = Profile.from_text(graphemes)

        # write grapheme profile to file
        with open(output_directory + '/' + name + '_graph.tsv', 'w', encoding='utf8', newline='') as output:
            output.write(str(profile_grapheme))

        profile_phoneme = Profile.from_text(phonemes)

        tokenizer = Tokenizer()

        # separate everything by # no matter if word or char as I want the chars in the end not the word
        ipa_segments = [re.sub(r'\s', '', x) for x in tokenizer(re.sub(r' ', '', phonemes),
                                                                ipa=True,
                                                                segment_separator='#').split('#')]

        # ipa cluster level
        counter_clusters = Counter(ipa_segments)

        # simple cluster level
        counter_simple_clusters = Counter([char.strip() for char in
                                           tokenizer(phonemes, segment_separator='#').split('#') if
                                           char != '#' and char != ' '])

        # code point level
        counter_phonemes = Counter([char.strip() for char in
                                    tokenizer.characters(phonemes) if char != '#' and char != ' '])

        with open(output_directory + '/' + name + '_ipa_clusters_l3.tsv', 'w', encoding='utf8') as output:
            output.write('Grapheme\tmapping\tfrequency\n')
            for seg, count in counter_clusters.most_common():
                output.write(seg + '\t' + seg + '\t' + str(count) + '\n')

        with open(output_directory + '/' + name + '_clusters_l2.tsv', 'w', encoding='utf8') as output:
            output.write('Grapheme\tmapping\tfrequency\n')
            for seg, count in counter_simple_clusters.most_common():
                output.write(seg + '\t' + seg + '\t' + str(count) + '\n')

        with open(output_directory + '/' + name + '_code_points_l1.tsv', 'w', encoding='utf8', newline='') as output:
            output.write('Grapheme\tmapping\tfrequency\n')
            for char, count in counter_phonemes.most_common():
                output.write(char + '\t' + char + '\t' + str(count) + '\n')


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    wikipron_to_lang_profiles(input_dir, output_dir)
