import unicodedata
import pandas as pd
from pathlib import Path
from segments.tokenizer import Tokenizer
from collections import Counter, OrderedDict

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


phoible = pd.read_csv('phoible.csv')
phonemes = phoible['Phoneme'].to_string(index=False)
chars = t.characters(phonemes)
pc = Counter(chars)

intersection = [phon for phon in c.keys() if phon not in pc.keys()]

print(intersection)

with open('phons_not_in_PHOIBLE.tsv', 'w', encoding='utf8') as out:
    out.write('phoneme' + '\t' + 'name' + '\n')
    for phon in intersection:
        # Value error raised when there is no Unicode name
        try:
            name = unicodedata.name(phon)
        except:
            name = 'NO NAME'
        out.write(phon + '\t' + name + '\n')

df = pd.DataFrame.from_dict(OrderedDict(c.most_common()), orient="index")
df.to_csv('phons_in_wikipron.csv')
