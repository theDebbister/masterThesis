#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import segments as seg
import re

from clean_wikipron_data import clean_phonemes


def transform_into_dict(transcript: str, ortho: str, output: str, language: str) -> None:
    """
    transforms a text and its corresponding phonetic transcription into a word-to-word-mapping
    :param transcript: path to phonetic transcription, one word per line
    :param ortho: path to orthographic version, one word per line
    :param output: output file name
    """

    with open(transcript, 'r', encoding='utf8') as trans, open(ortho, 'r', encoding='utf8') as ortho:
        transcript_lines = trans.readlines()
        ortho_lines = ortho.readlines()


    ortho_tokens = []
    for line in ortho_lines:
        # clean out punctuation
        ortho_tokens.extend(re.sub(r'[:;.,!?，。、\(\)「」’]', '', line.lower()).split())
        
    trans_tokens = []
    tokenizer = seg.Tokenizer()

    for line in transcript_lines:
        token = tokenizer(line, ipa=True)
        token = clean_phonemes([token], language)
        if token[0]:
            # splits the phon token into ipa segments, sep by space
            trans_tokens.append(token[0])

    # need to manually check cases where grapheme-phoneme mapping does not work
    if len(trans_tokens) == len(ortho_tokens):
        with open(output + '.tsv', 'w', encoding='utf8') as output:
            for t, o in zip(trans_tokens, ortho_tokens):
                output.write(o.strip(' .') + '\t' + t.strip(' .') + '\n')
    else:
        print('COULD NOT CREATE DICT FOR', output)
        for t in trans_tokens:
            print(t)
        print(f'Num tokens phonetic: {len(trans_tokens)}\t Num tokens orthographic: {len(ortho_tokens)}')


if __name__ == '__main__':
    t = sys.argv[1]
    o = sys.argv[2]
    output = sys.argv[3]
    lang = sys.argv[4]
    
    transform_into_dict(t, o, output, lang)
