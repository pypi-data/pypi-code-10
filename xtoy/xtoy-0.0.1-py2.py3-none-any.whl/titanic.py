
import re


test = {tuple(sorted(re.findall('[a-z]+', x.lower()))): x for x in Xtest[:, 2]}

with open('/Users/pascal/GDrive/xtoy/real.txt') as f:
    data = {tuple(sorted(re.findall('[a-z]+', ' '.join(x.split()[:4]).lower())))
                  : x.split()[-4:] for x in f.read().splitlines()[1:]}


def ldist(w, listy):
    return sorted([(x, Levenshtein.distance(x, w)) for x in listy], key=lambda x: x[1])

it = 0
jdata = [' '.join(x) for x in data]
for x in test:
    print(x, ldist(' '.join(x), jdata)[0])
