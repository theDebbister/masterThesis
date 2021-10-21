import sys
import segments as seg


def transform_into_dict(transcript:str, ortho: str, output):
    with open(transcript, 'r', encoding='utf8') as trans, open(ortho, 'r', encoding='utf8') as ortho:
        transcript_lines = trans.readlines()
        ortho_lines = ortho.readlines()
        
    ortho_tokens = []
    for line in ortho_lines:
        ortho_tokens.extend(line.lower().split())
        
    trans_tokens = []
    lang_profile = seg.Profile().from_textfile(transcript)
    for line in transcript_lines:
        tokenizer = seg.Tokenizer(lang_profile)
        tokens = tokenizer(line)
        trans_tokens.extend(tokens.split('#'))
        
    if len(trans_tokens) == len(ortho_tokens):
        with open(output + '.dict', 'w', encoding='utf8') as output:
            for t, o in zip(trans_tokens, ortho_tokens):
                output.write(o.strip(' .') + '\t' + t.strip(' .') + '\n')
    else:
        print('COULD NOT CREATE DICT FOR', output)
        for t in trans_tokens:
            print(t)
        print(len(trans_tokens), len(ortho_tokens))
        
        

if __name__ == '__main__':
    t = sys.argv[1]
    o = sys.argv[2]
    output = sys.argv[3]
    
    transform_into_dict(t, o, output)