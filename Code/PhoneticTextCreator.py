import re

import pandas as pd
from io import TextIOWrapper


class PhoneticTextCreator:

    def __init__(self, wordlist: TextIOWrapper, text: TextIOWrapper):
        self.wordlist = self._prepare_wordlist(wordlist)
        self.text = self._preprocess_text(text)

        self.percentage = 0

    @staticmethod
    def _preprocess_text(text) -> [str]:
        text = text.read()
        text = text.lower()
        text = re.sub(r'[\?!:;\.,\"\(\)]', "", text)
        text = re.sub(r'[\'\-]', " ", text)
        text = text.split()

        return text

    @staticmethod
    def _prepare_wordlist(wordlist: TextIOWrapper) -> dict:
        df_wordlist = pd.read_csv(wordlist, sep='\t', names=['word', 'pronunciation'])

        vocabulary = dict(zip(df_wordlist.word, df_wordlist.pronunciation))

        return vocabulary

    def get_phonetic_text(self):
        return self.text

    def create_phonetic_text(self):
        phonetic_text = ""

        count_exist = 0
        count_not_exist = 0

        for word in self.text:
            if word.strip() in self.wordlist:
                phonetic_text += re.sub(r' ', '', self.wordlist[word]) + " "
                count_exist += 1
            else:
                splittable = False

                # exclude the split of the first and last character separately
                for n in range(len(word.strip()) - 3):
                    w1 = word[:n + 2]
                    w2 = word[n + 2:]
                    if w1 in self.wordlist and w2 in self.wordlist:
                        phonetic_text += self.wordlist[w1] + self.wordlist[w2] + " "
                        splittable = True
                        count_exist += 1
                        print(w1, w2, self.wordlist[w1], self.wordlist[w2])
                        break

                if not splittable:
                    phonetic_text += word.upper() + " "
                    count_not_exist += 1

        self.percentage = round((count_exist / (count_not_exist + count_exist)) * 100, 2)

        return phonetic_text, self.percentage
