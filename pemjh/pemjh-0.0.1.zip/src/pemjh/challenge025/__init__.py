""" Challenge025 """
from pemjh.utilities.numbers import fibo
from itertools import dropwhile


def challenge025():
    """ challenge025 """
    return dropwhile(lambda x: len(str(x[1])) < 1000,
                     enumerate(fibo(), start=1)).next()[0]
