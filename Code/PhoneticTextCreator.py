import codecs
import re
import unicodedata

import pandas as pd
import csv
import jiwer
import Levenshtein as lev
import hebrew_tokenizer as heb_tok
from spacy.lang.zh import Chinese
from spacy.lang.en import English


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

                phonetic_text, per_transcribed, per_concat, per_unk = self._create_phonetic_text(path_org,
                                                                                                 path_wordlist,
                                                                                                 lang)

                wer = round(jiwer.wer(ref_text, phonetic_text), 2)

                cer_val = round(cer(ref_text, phonetic_text), 2)

                with open(new_file_name, 'w', encoding='utf8') as new_phonetic:
                    new_phonetic.write(phonetic_text)

                new_row = [lang, per_transcribed, per_concat, per_unk, wer, cer_val,
                           path_org, path_wordlist, new_file_name, type_ref, type_list]

                data_writer.writerow(new_row)

                new_stats_row = [lang, per_transcribed, wer, cer_val, type_ref, type_list, num_w]

                stats_writer.writerow(new_stats_row)

    def _prepare_output_file(self):
        header = ['lang-code (iso 639-3)', 'coverage', 'per-concat', 'per-unk', 'WER', 'CER', 'path-original',
                  'path-wordlist', 'path-phonetic-text', 'type-ref', 'type-list']

        stats_header = ['Iso 639-3', 'Coverage', 'WER', 'CER', 'Type ref', 'Type list', 'Num words list']

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
            # Language specific tokenizers
            if lang == 'cmn':
                nlp = Chinese()
                tokenizer = nlp.tokenizer
                for token in tokenizer(text):
                    tokens.append(str(token))
            else:
                text = text.lower()
                text = re.sub(r'[\?!:;\.,\"\(\)]', "", text)
                text = re.sub(r'[\'\-。，]', " ", text)
                tokens = text.split()

        # in case that the fil encoding is wrong
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
        text = self._preprocess_text(path_original, lang)

        wordlist = self._prepare_wordlist(wordlist)

        phonetic_text = ""

        count_exist = 0
        count_not_exist = 0
        count_concat = 0

        for word in text:
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

        return phonetic_text, per_transcribed, per_concat, per_unk
