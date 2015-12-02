""" Challenge082 """
from __future__ import with_statement
from os.path import abspath, dirname


def combine_columns(c1, c2):
    down_row = list()

    # Step through c2
    previous = None
    for v1, v2 in zip(c1, c2):
        possibles = list()
        if previous is not None:
            possibles.append(previous + v2)
        # The straight route is v1, v2
        possibles.append(v1 + v2)

        lowest = min(possibles)
        previous = lowest

        down_row.append(lowest)

    new_row = list()

    previous = None
    for v1, v2 in zip(reversed(down_row), reversed(c2)):
        possibles = list()
        if previous is not None:
            possibles.append(previous + v2)
        possibles.append(v1)

        lowest = min(possibles)
        previous = lowest

        new_row.append(lowest)

    return list(reversed(new_row))


def challenge082():
    """ challenge082 """
    # Open the file
    path = "%s/matrix.txt" % dirname(abspath(__file__))
    with open(path) as f:
        # Read row data
        rows = [[int(i) for i in l.strip().split(",")] for l in f]
        # Convert to columns
        columns = [list(l) for l in zip(*rows)]
        # Reduce the columns
        return min(reduce(combine_columns, columns))
