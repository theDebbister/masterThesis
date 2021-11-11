import sys

from pathlib import Path
import pandas as pd
from segments.tokenizer import Tokenizer
from collections import Counter

p = Path('wikipron_100LC/high/').rglob('*.tsv')

t = Tokenizer()
c = Counter()


for filepath in p: 
    print(filepath)    
    df = pd.read_csv(filepath, delimiter='\t', names=['graphemes', 'phonemes'],
                          dtype={'graphemes': str, 'phonemes': str}, na_filter=False)
    s = df['phonemes'].to_string(index=False)
    chars = t.characters(s)
    c.update(s)
print(c)


phoible = pd.read_csv('phoible.csv')
phonemes = phoible['Phoneme'].to_string(index=False)
chars = t.characters(phonemes)
pc = Counter(chars)
print(pc)

# Take the intersection and see what's in Wikiphon and not in phoible