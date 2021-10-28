import sys
from segments import Profile


def get_stats(profile1, profile2):
    prf1 = Profile.from_file(profile1)
    prf2 = Profile.from_file(profile2)

    l1 = [p for p in prf1.iteritems()]
    l2 = [p for p in prf2.iteritems()]

    intersect = [x['Grapheme'] for x in l1 if x['Grapheme'] in [y['Grapheme'] for y in l2]]


    l1_only = [x['Grapheme'] for x in l1 if x['Grapheme'] not in intersect]
    l2_only = [x['Grapheme'] for x in l2 if x['Grapheme'] not in intersect]

    percentage_l1_in_l2 = (len(intersect) / len(l1)) * 100
    percentage_l2_not_in_l1 = (len(l2_only) / len(l2)) * 100

    print(f'Intersection of profile 1 and profile 2: {intersect}')
    print(f'Percentage of characters profile 1 (train) that is covered in profile 2 (test): {round(percentage_l1_in_l2, 2)}%')
    print(f'Percentage of characters profile 2 (test) that is not in profile 1 (train): {round(percentage_l2_not_in_l1, 2)}%')


if __name__ == '__main__':
    p1 = sys.argv[1]
    p2 = sys.argv[2]
    get_stats(p1, p2)
