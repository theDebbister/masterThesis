import pandas as pd
from collections import Counter, OrderedDict


def extract_phoible_phonemes():
    path = 'phoible.csv'
    dataset = pd.read_csv(path, index_col=False, dtype=str)
    only_features_and_phonemes = dataset[['Phoneme', "tone", "stress", "syllabic", "short", "long", "consonantal",
                                          "sonorant", "continuant", "delayedRelease", "approximant", "tap", "trill",
                                          "nasal",
                                          "lateral", "labial", "round", "labiodental", "coronal", "anterior",
                                          "distributed",
                                          "strident", "dorsal", "high", "low", "front", "back", "tense",
                                          "retractedTongueRoot",
                                          "advancedTongueRoot", "periodicGlottalSource", "epilaryngealSource",
                                          "spreadGlottis", "constrictedGlottis", "fortis", "raisedLarynxEjective",
                                          "loweredLarynxImplosive", "click"]]

    phonemes = only_features_and_phonemes['Phoneme'].to_list()

    codes = dataset['ISO6393'].to_list()

    features_vectors = dataset[["tone", "stress", "syllabic", "short", "long", "consonantal",
                                "sonorant", "continuant", "delayedRelease", "approximant", "tap", "trill",
                                "nasal",
                                "lateral", "labial", "round", "labiodental", "coronal", "anterior",
                                "distributed",
                                "strident", "dorsal", "high", "low", "front", "back", "tense",
                                "retractedTongueRoot",
                                "advancedTongueRoot", "periodicGlottalSource", "epilaryngealSource",
                                "spreadGlottis", "constrictedGlottis", "fortis", "raisedLarynxEjective",
                                "loweredLarynxImplosive", "click"]]
    unique_features = features_vectors.drop_duplicates()
    features_vectors_list = features_vectors.values.tolist()

    print(len(phonemes), len(codes), len(features_vectors_list))

    l = []
    phonemes_set = []

    for p, v in zip(phonemes, features_vectors_list):
        if p not in phonemes_set:
            phonemes_set.append(p)
            p = [p]
            p.extend(v)
            l.append(p)

    df = pd.DataFrame(l)

    df.to_csv('phoible_features.csv', index=False, header=['Phoneme', "tone", "stress", "syllabic", "short", "long", "consonantal",
                                          "sonorant", "continuant", "delayedRelease", "approximant", "tap", "trill",
                                          "nasal",
                                          "lateral", "labial", "round", "labiodental", "coronal", "anterior",
                                          "distributed",
                                          "strident", "dorsal", "high", "low", "front", "back", "tense",
                                          "retractedTongueRoot",
                                          "advancedTongueRoot", "periodicGlottalSource", "epilaryngealSource",
                                          "spreadGlottis", "constrictedGlottis", "fortis", "raisedLarynxEjective",
                                          "loweredLarynxImplosive", "click"])





if __name__ == '__main__':
    extract_phoible_phonemes()
