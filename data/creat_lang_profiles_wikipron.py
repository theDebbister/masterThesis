import sys
import os
import pandas as pd
from segments import Profile


def wikipron_to_lang_profiles(directory: str, output_directory: str):

    for filename in os.listdir(directory):
        name = filename[:-4]
        tsv = pd.read_csv(directory + '/' + filename, delimiter='\t', names=['graphemes', 'phonemes'],
                          dtype={'graphemes': str, 'phonemes': str})

        print(tsv[tsv.isna().any(axis=1)])


        phonemes = tsv['phonemes'].to_list()
        graphemes = tsv['graphemes'].to_list()

        grapheme = ''

        for g in graphemes:
            if type(g) == float:
                print(g)
            #grapheme += g

        profile_grapheme = Profile.from_text(grapheme)
        #     #with open(output_directory + '/' + name + '_graphemes.prf', 'w', encoding='utf8', newline='') as output:
        #      #   output.write(str(profile_grapheme))
        # except TypeError:
        #     print(filename)
        #     print('grapheme')


        profile_phoneme = Profile.from_text(' '.join(phonemes))
        #     with open(output_directory + '/' + name + '_phonemes.prf', 'w', encoding='utf8', newline='') as output:
        #         output.write(str(profile_phoneme))
        # except TypeError:
        #     print(filename)
        #     print('phoneme')






if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    wikipron_to_lang_profiles(input_dir, output_dir)
