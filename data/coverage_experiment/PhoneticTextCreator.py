import codecs
import re
import unicodedata

import pandas as pd
import csv
import numpy as np
from tabulate import tabulate
import Levenshtein as lev


# Applies to lines 31 - 44
# MIT License
#
# Copyright (c) 2021 Deborah Jakobi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://github.com/jpuigcerver/xer --> source of lines 31 - 44
def per_score(gold, hypo) -> (int, int):
    """Computes sufficient statistics for LER calculation."""
    edits = edit_distance(gold, hypo)
    return edits, len(gold)


def edit_distance(x, y) -> int:
    # For a more expressive version of the same, see:
    #
    #     https://gist.github.com/kylebgorman/8034009
    idim = len(x) + 1
    jdim = len(y) + 1
    table = np.zeros((idim, jdim), dtype=np.uint8)
    table[1:, 0] = 1
    table[0, 1:] = 1
    for i in range(1, idim):
        for j in range(1, jdim):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                c1 = table[i - 1][j]
                c2 = table[i][j - 1]
                c3 = table[i - 1][j - 1]
                table[i][j] = min(c1, c2, c3) + 1
    return int(table[-1][-1])


def create_g2p_gt_map(words, pronunciations):
    """Create grapheme-to-phoneme ground true mapping."""
    g2p_gt_map = {}
    for word, pronunciation in zip(words, pronunciations):
        if word in g2p_gt_map:
            g2p_gt_map[word].append(pronunciation)
        else:
            g2p_gt_map[word] = [pronunciation]
    return g2p_gt_map


def calc_errors(inputs, decodes, words, pronunciations):
    """Calculate a number of prediction errors."""

    g2p_gt_map = create_g2p_gt_map(words, pronunciations)

    correct, errors = 0, 0
    num_edits, len_reference = 0, 0
    not_in_test = 0

    for index, word in enumerate(inputs):

        try:
            if decodes[index] in g2p_gt_map[word]:
                correct += 1
                num_edits += 0
                len_reference += len(decodes[index])
            else:
                errors += 1
                smallest_per = 200
                best_len = 0
                best_edit = 0
                for ref in g2p_gt_map[word]:
                    temp_edit, temp_len = per_score(ref, decodes[index])
                    temp_per = 100 * temp_edit / temp_len
                    if temp_per < smallest_per:
                        smallest_per = temp_per
                        best_len = temp_len
                        best_edit = temp_edit
                num_edits += best_edit
                len_reference += best_len
        except KeyError:
            not_in_test += 1

    return correct, errors, num_edits, len_reference

def cer(hypothesis, reference):
    cer_s, cer_i, cer_d, cer_n = 0, 0, 0, 0
    # update CER statistics
    stats = lev.opcodes(reference, hypothesis)
    for op in stats:
        if op[0] == 'replace':
            cer_s += op[2] - op[1]
        elif op[0] == 'insert':
            cer_i += 1
        elif op[0] == 'delete':
            cer_d += op[2] - op[1]
    cer_n = len(reference)

    return (cer_s + cer_i + cer_d) / cer_n


class PhoneticTextCreator:

    def __init__(self, text: str, wordlist='', lang='', name='', concat=False):
        self.percentage = []
        self.preprocessed_text = []
        self.phonetic_text = []
        self.preprocessed_wordlist = []
        self.lang = lang
        self.name = name
        self.concat = concat
        self.output_name = "overview" + ('_' if self.name else '') + self.name + ".tsv"
        self.stats_name = "stats" + ('_' if self.name else '') + self.name + ".csv"

        if not wordlist:
            self._prepare_output_file()
            self.csv_file = text
            self._process_csv()
        else:
            self._create_phonetic_text(text, wordlist, self.lang)

    def _process_csv(self) -> None:
        with open(self.csv_file, 'r', encoding='utf8') as file, \
                open(self.output_name, 'a', encoding='utf8', newline='') as output, \
                open(self.stats_name, 'a', encoding='utf8', newline='') as stats:
            data_reader = csv.reader(file, delimiter=';')
            data_writer = csv.writer(output, delimiter='\t')
            stats_writer = csv.writer(stats, delimiter=',')

            all_langs = []
            num = 0
            for row in data_reader:
                lang, path_org, path_wordlist, reference, type_ref, type_list, num_w = row[0], row[1], row[2], \
                                                                                       row[3], row[4], row[5], row[6]
                print(lang)
                with open(reference, 'r', encoding='utf8') as r:
                    ref_text = r.read()

                # differentiate texts of same languages
                if lang not in all_langs:
                    all_langs.append(lang)
                    num = 0
                else:
                    num += 1

                # create new file name including the custom name
                new_file_name = 'output/' + lang + '_' + str(num) + '_phonetic' + (
                    '_' if self.name else '') + self.name + '.txt'

                phonetic_text, per_transcribed, per_concat, per_unk, original_tokens = self._create_phonetic_text(path_org,
                                                                                                 path_wordlist,
                                                                                                 lang)
                inputs = original_tokens
                dec = phonetic_text.split()
                words = original_tokens
                pron = ref_text.split()

                correct, errors, edits, len_reference = calc_errors(inputs, dec, words, pron)

                wer = round(float(errors) / (correct + errors) * 100, 2)
                per = round((float(edits) / len_reference) * 100, 2)

                with open(new_file_name, 'w', encoding='utf8') as new_phonetic:
                    new_phonetic.write(phonetic_text)

                new_row = [lang, per_transcribed, per_concat, per_unk, wer, per,
                           path_org, path_wordlist, new_file_name, type_ref, type_list]

                data_writer.writerow(new_row)

                new_stats_row = [lang, per_transcribed, wer, per, type_ref, type_list, num_w]

                stats_writer.writerow(new_stats_row)

        # print stats as latex table to include into thesis
        s = pd.read_csv(self.stats_name, index_col=False)
        print(s.to_latex(index=False))

    def _prepare_output_file(self):
        header = ['lang-code (iso 639-3)', 'coverage', 'per-concat', 'per-unk', 'WER', 'PER', 'path-original',
                  'path-wordlist', 'path-phonetic-text', 'type-ref', 'type-list']

        stats_header = ['Iso 639-3', 'Coverage', 'WER', 'PER', 'Type ref', 'Type list', 'Num words list']

        with open(self.output_name, 'w', newline='') as output:
            writer = csv.writer(output, delimiter='\t')
            writer.writerow(header)

        with open(self.stats_name, 'w', newline='') as output:
            writer = csv.writer(output, delimiter=',')
            writer.writerow(stats_header)

    @staticmethod
    def _preprocess_text(path_original: str, lang: str) -> [str]:
        """
        preprocesses the original text: remove punctuation, tokenize and lower case
        :param path_original:
        :param lang:
        :return:
        """
        tokens = []

        try:
            with open(path_original, 'r', encoding='utf8') as text_file:
                text = text_file.read()

            text = text.lower()
            text = re.sub(r'[\?!:;\.,\"\(\)]', "", text)
            text = re.sub(r'[\'\-。，]', " ", text)
            tokens = text.split()


        # in case that the file encoding is wrong
        except UnicodeDecodeError:
            print(path_original)

        return tokens

    @staticmethod
    def _prepare_wordlist(wordlist: str) -> dict:
        df_wordlist = pd.read_csv(wordlist, sep='\t', names=['word', 'pronunciation'])

        vocabulary = dict(zip(df_wordlist.word, df_wordlist.pronunciation))

        return vocabulary

    def get_phonetic_text(self):
        pass

    def _create_phonetic_text(self, path_original, wordlist, lang):
        tokens = self._preprocess_text(path_original, lang)

        wordlist = self._prepare_wordlist(wordlist)

        phonetic_text = ""

        count_exist = 0
        count_not_exist = 0
        count_concat = 0

        for word in tokens:
            splittable = False

            if word.strip() in wordlist:
                phonetic_text += re.sub(r' ', '', wordlist[word]) + " "
                count_exist += 1
            elif self.concat:
                # exclude the split of the first and last character separately
                for n in range(len(word.strip()) - 3):
                    w1 = word[:n + 2]
                    w2 = word[n + 2:]
                    if w1 in wordlist and w2 in wordlist:
                        phonetic_text += re.sub(r' ', '', wordlist[w1]) + re.sub(r' ', '', wordlist[w2]) + " "
                        splittable = True
                        count_concat += 1
                        count_exist += 1
                        break
                if not splittable:
                    phonetic_text += word.upper() + " "
                    count_not_exist += 1

            else:
                phonetic_text += word.upper() + " "
                count_not_exist += 1

        per_transcribed = round((count_exist / (count_not_exist + count_exist + count_concat)) * 100, 2)
        per_concat = round((count_concat / (count_not_exist + count_exist + count_concat)) * 100, 2)
        per_unk = round((100 - per_transcribed), 2)

        self.percentage.append(per_transcribed)
        self.phonetic_text.append(phonetic_text)

        return phonetic_text, per_transcribed, per_concat, per_unk, tokens
