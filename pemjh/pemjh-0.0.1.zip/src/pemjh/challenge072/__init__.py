""" Challenge072 """
from pemjh.utilities.numbers import phi


def challenge072():
    """ challenge072 """
    limit = 1000000
    return int(sum(phi(limit)) - 1)
