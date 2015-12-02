""" Challenge117 """
from pemjh.utilities.numbers import numVariations


def process(blocks):
    n = numVariations(blocks, [2, 3, 4], dict())
    return n


def challenge117():
    """ challenge117 """
    blocks = 50
    return process(blocks)
