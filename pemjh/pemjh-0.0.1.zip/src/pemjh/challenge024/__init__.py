""" Challenge024 """
from pemjh.utilities.strings import permutate
from itertools import islice


def challenge024():
    """ challenge024 """
    number = "0123456789"
    return int(list(islice(permutate(number), 999999, 1000000))[0])
