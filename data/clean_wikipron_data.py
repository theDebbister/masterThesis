#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import pandas as pd
import sys
from pathlib import Path
import re
from segments.tokenizer import Tokenizer
from collections import Counter, OrderedDict
from tqdm import tqdm


def clean_data(data_path):
    wikipron_path = Path(data_path).rglob('*.tsv')

    for file in tqdm(list(wikipron_path)):

        lang = file.name[:3]

        # cleaning that is done for all languages
        current_lang = pd.read_csv(file, sep='\t', names=['grapheme', 'phonemes'])

        # remove duplicates and keep the last occurence
        current_lang.drop_duplicates(subset=['grapheme'], keep='last', inplace=True)

        old_phonemes = current_lang['phonemes'].to_list()

        current_lang['phonemes'] = clean_phonemes(old_phonemes, lang)

        current_lang.to_csv('wikipron_clean/v2/' + file.name, sep='\t', index=False, header=None)


def clean_phonemes(phonemes: list, language: str) -> list:
    t = Tokenizer()
    new_phonemes = []

    for phon in phonemes:
        phon = unicodedata.normalize('NFD', phon)
        if ',' in phon:
            comma = phon.find(',')
            phon = phon[:comma]
        if '⁓' in phon:
            dash = phon.find('⁓')
            phon = phon[:dash]

        phones = phon.split()
        new_ph = ''

        for ph in phones:
            ph = re.sub(r'[ˈ̋́́ ̄̀ ̏ꜜꜛꜜ̌̂᷄ ᷅᷈]', '', ph)
            ph = re.sub(r'[⁵¹²³⁴⁻⁽⁾⁰̍͜͡‿ʸ↘↗˥˦˧˨˩˩˥˥˩˧˥˩˧˧˦˨|‖|ˌᵊ˔~ᵑᶢ]', '', ph)
            ph = re.sub(r'ɝ', 'ɚ', ph)
            ph = re.sub(r'g', 'ɡ', ph)
            ph = re.sub(r'à', 'a', ph)
            ph = re.sub(r'á', 'a', ph)
            ph = re.sub(r'è', 'e', ph)
            ph = re.sub(r'é', 'e', ph)
            ph = re.sub(r'ì', 'ɪ', ph)
            ph = re.sub(r'í', 'ɪ', ph)
            ph = re.sub(r'\.', '', ph)

            # some language specific cleaning for Finnish
            if language == 'fin':
                ph = re.sub(r'ˣ', 'ʔ', ph)

            new_ph += ph.strip()

        new_ph = t(new_ph, ipa=True)
        if r'  ' in new_ph:
            print(phon, new_ph)

        new_phonemes.append(new_ph.strip())

    return new_phonemes


if __name__ == '__main__':
    p = sys.argv[1]

    clean_data(p)