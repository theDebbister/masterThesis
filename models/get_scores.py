import pandas as pd
import sys
from tabulate import tabulate

input_file = sys.argv[1]

# I used this script to extract the score from the scores eval files and put them in a nice table format

with open(input_file, 'r', encoding='utf8') as f:

    wer = 0
    per = 0
    lang = ''
    table = []

    for line in f:
        if line.startswith('WER'):
            wer = round(float(line[-6:].strip()) * 100, 1)

        elif line.startswith('PER'):
            per = round(float(line[-6:].strip()) * 100, 1)

        elif line.startswith('Lang:'):
            lang = line[5:].strip()
            row = [lang, wer, per]
            table.append(row)
            wer = 0
            per = 0
            lang = ''

    print(tabulate(table))
