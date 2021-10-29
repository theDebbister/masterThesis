import sys
import os
import pandas as pd
from segments import Profile
from segments import Tokenizer
from collections import Counter
import re


def wikipron_to_lang_profiles(directory: str, output_directory: str):

    for filename in os.listdir(directory):
        name = filename[:-4]
        tsv = pd.read_csv(directory + '/' + filename, delimiter='\t', names=['graphemes', 'phonemes'],
                          dtype={'graphemes': str, 'phonemes': str}, na_filter=False)



        phonemes = tsv['phonemes'].to_list()
        graphemes = tsv['graphemes'].to_list()


        profile_grapheme = Profile.from_text(' '.join(graphemes))
        with open(output_directory + '/' + name + '_graph.prf', 'w', encoding='utf8', newline='') as output:
           output.write(str(profile_grapheme))



        profile_phoneme = Profile.from_text(' '.join(phonemes))
        
        t = Tokenizer(profile=profile_phoneme)
        ipa_segments = [re.sub(' ', '', x) for x in t(' '.join(phonemes)).split('#')]

        c = Counter(ipa_segments)

        with open(output_directory + '/' + name + '_phon_clusters.prf', 'w', encoding='utf8') as output:
            output.write('Grapheme\tmapping\tfrequency\n')
            for seg, count in c.most_common():
                output.write(seg + '\t' + seg + '\t' + str(count) + '\n')

        with open(output_directory + '/' + name + '_phon.prf', 'w', encoding='utf8', newline='') as output:
             output.write(str(profile_phoneme))




if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    wikipron_to_lang_profiles(input_dir, output_dir)
