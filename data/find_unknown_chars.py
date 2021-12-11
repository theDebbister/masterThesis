#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import pandas as pd
from pathlib import Path
from segments.tokenizer import Tokenizer
from collections import Counter, OrderedDict
from tqdm import tqdm

p_wikipron = Path('wikipron_clean/v2/').rglob('*.tsv')
p_unknown_chars = 'phons_not_in_PHOIBLE_raw.tsv'

chars_unknown = pd.read_csv(p_unknown_chars, sep='\t', na_filter=False)['phoneme'].to_list()

t = Tokenizer()

d = {}


for filepath in tqdm(list(p_wikipron)):
    df = pd.read_csv(filepath, delimiter='\t', names=['graphemes', 'phonemes'],
                          dtype={'graphemes': str, 'phonemes': str}, na_filter=False)
    s = unicodedata.normalize('NFD', df['phonemes'].to_string(index=False))
    chars = t.characters(s)
    counts = Counter(chars)

    d[filepath] = Counter({k: v for k, v in counts.items() if k in chars_unknown}).most_common()


with open('unknown_chars_in_wikipron.txt', 'w', encoding='utf8') as out:
    for (k, v) in d.items():
        if v:
            out.write('\n' + k.name + '\n')
            for k2, v2 in v:
                try:
                    name = unicodedata.name(k2)
                except ValueError:
                    name = 'NO NAME'
                out.write(f'{k2}\t{v2}\t{name}\n')


