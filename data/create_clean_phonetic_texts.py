

import pandas as pd
from pathlib import Path
import re

# I used this script to create clean phonetic full texts for the nws stories from the dictionaries.

nws_paths = Path('nws_test_dicts_clean/').rglob('*.tsv')

for path in nws_paths:
    tsv = pd.read_csv(path, sep='\t', names=['graphemes', 'phonemes'])
    phonemes = '#'.join(tsv.phonemes.tolist())

    phonemes = re.sub(r' ', '', phonemes)
    phonemes = re.sub(r'#', ' ', phonemes)

    name = path.name[:-4]

    with open(f'nws_clean_phonetic/{name}.txt', 'w', encoding='utf8') as out:
        out.write(phonemes)
