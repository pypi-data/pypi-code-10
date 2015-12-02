""" Challenge139 """
from pemjh.utilities.numbers import getPrimitiveTriples


def challenge139():
    """ challenge139 """
    maximum_size = 100000000

    total = 0
    for a, b, c in getPrimitiveTriples(maximum_size):

        if c % (b - a) == 0:
            # Fills...
            total += maximum_size // (a + b + c)

    return total
