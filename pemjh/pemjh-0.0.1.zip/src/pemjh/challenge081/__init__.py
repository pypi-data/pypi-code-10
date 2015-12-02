""" Challenge081 """
from __future__ import with_statement
from os.path import abspath, dirname


def add_rows(rows):
    """ Reduce all rows into 1 """
    while len(rows) > 1:
        row1 = rows[0]
        row2 = rows[1]

        for i in xrange(0, len(row2)):
            i1 = row1[i - 1] if i != 0 else row1[i]
            i2 = row1[i] if i != len(row2) - 1 else row1[i - 1]

            row2[i] = i1 + row2[i] if i1 < i2 else i2 + row2[i]

        rows = rows[1:]

    return rows[0]


def challenge081():
    """ challenge081 """
    side = 80
    with open("%s/matrix.txt" % dirname(abspath(__file__))) as f:
        tr = list()
        for i in xrange(2 * side - 1):
            tr.append(list())

        for n, l in enumerate(l for l in f):
            index = n
            for i in [int(j) for j in l.split(",")]:
                tr[index].append(i)
                index += 1

    # Get 0:80
    tr1 = tr[0:side]
    tr1 = add_rows(tr1)
    # Get 81:
    tr2 = list(reversed(tr[side:]))
    tr2 = add_rows(tr2)

    tr = add_rows([tr2, tr1])

    return min(tr)
