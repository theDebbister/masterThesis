import re
import pandas as pd
from io import TextIOWrapper
import csv


class PhoneticTextCreator:

    def __init__(self, text: str, csv=False, wordlist=''):
        self.csv = csv
        self.percentage = []
        self.preprocessed_text = []
        self.phonetic_text = []
        self.preprocessed_wordlist = []

        if self.csv:
            self.csv_file = text
            self._process_csv()
        else:
            self._create_phonetic_text(text, wordlist)

    def _process_csv(self):
        with open(self.csv_file, 'r', encoding='utf8') as file:
            data_reader = csv.reader(file, delimiter=',')
            for row in data_reader:
                self._create_phonetic_text(row[0], row[1])

    @staticmethod
    def _preprocess_text(text: str) -> [str]:
        with open(text, 'r', encoding='utf8') as text_file:
            text = text_file.read()
        text = text.lower()
        text = re.sub(r'[\?!:;\.,\"\(\)]', "", text)
        text = re.sub(r'[\'\-]', " ", text)
        text = text.split()

        return text

    @staticmethod
    def _prepare_wordlist(wordlist: str) -> dict:
        df_wordlist = pd.read_csv(wordlist, sep='\t', names=['word', 'pronunciation'])

        vocabulary = dict(zip(df_wordlist.word, df_wordlist.pronunciation))

        return vocabulary

    def get_phonetic_text(self):
        return self.text

    def _create_phonetic_text(self, text, wordlist):
        text = self._preprocess_text(text)
        self.preprocessed_text.append(text)

        wordlist = self._prepare_wordlist(wordlist)
        self.preprocessed_wordlist.append(wordlist)

        phonetic_text = ""

        count_exist = 0
        count_not_exist = 0

        for word in text:
            if word.strip() in wordlist:
                phonetic_text += re.sub(r' ', '', wordlist[word]) + " "
                count_exist += 1
            else:
                splittable = False

                # exclude the split of the first and last character separately
                for n in range(len(word.strip()) - 3):
                    w1 = word[:n + 2]
                    w2 = word[n + 2:]
                    if w1 in wordlist and w2 in wordlist:
                        phonetic_text += wordlist[w1] + wordlist[w2] + " "
                        splittable = True
                        count_exist += 1
                        break

                if not splittable:
                    phonetic_text += word.upper() + " "
                    count_not_exist += 1

        self.percentage.append(round((count_exist / (count_not_exist + count_exist)) * 100, 2))
        self.phonetic_text.append(phonetic_text)

    def create_csv(self):
        d = {'preprocessed-text': [' '.join(text) for text in self.preprocessed_text],
             'wordlist': self.preprocessed_wordlist,
             'Phonetic-text': self.phonetic_text,
             'Percentage of words in pron dict': self.percentage,
             }

        df = pd.DataFrame(d)

        df.to_csv("example_output.csv", index=False)
        print('Created csv output')
