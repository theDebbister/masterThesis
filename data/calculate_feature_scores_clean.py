#!/usr/bin/python
# -*- coding: utf-8 -*-

import unicodedata
import pandas as pd
import sys
import numpy as np
from pathlib import Path
import re
from collections import Counter, OrderedDict
from tqdm import tqdm


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


def clean_data(predictions):

    with open(predictions, 'r', encoding='utf8') as pred:

        inputs = []
        dec = []

        last_lines = []

        end_of_data = False
        counter = 6

        for line in pred:

            if counter == 0:
                counter = 6
                end_of_data = False
                lang = re.sub(r'Lang: ', '', last_lines[-1])

                #if not lang == 'vie_latn_hanoi_narrow_filtered':

                gold_df = pd.read_csv('gold/' + lang + '.tsv.part.test', sep='\t', names=['word', 'pron'])

                words = gold_df['word'].to_list()
                pron = gold_df['pron'].to_list()

                correct, errors, edits, len_reference = calc_errors(inputs, dec, words, pron)

                print(f'Lang: {lang}')
                print("Words: %d" % (correct + errors))
                print("Errors: %d" % errors)
                print("WER: %.3f" % (float(errors) / (correct + errors)))
                print("PER: %.3f" % (float(edits) / len_reference))
                print("Accuracy: %.3f" % float(1. - (float(errors) / (correct + errors))))
                print('------------------------')

                inputs = []
                dec = []
                last_lines = []

            elif end_of_data:
                last_lines.append(line.strip())
                counter -= 1

            elif line.startswith('Words:'):
                end_of_data = True
                last_lines.append(line.strip())
                counter -= 1

            elif not end_of_data and line != '\n':
                line = line.split('\t')
                inputs.append(line[0])

                phon = line[1].strip()
                phon = re.sub(r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ][ABCDEFGHIJKLMNOPQRSTUVWXYZ]', '', phon)
                phon = re.sub(r'(\s+)', ' ', phon)
                dec.append(phon.strip())


if __name__ == '__main__':
    predictions_path = sys.argv[1]

    clean_data(predictions_path)

