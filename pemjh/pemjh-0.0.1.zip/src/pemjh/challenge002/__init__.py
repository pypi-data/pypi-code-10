""" Challenge002 """
from pemjh.utilities.numbers import fibo
from itertools import takewhile


def challenge002():
    """ challenge002 """
    number_range = takewhile(lambda i: i < 4000000, fibo())
    even_numbers = (i for i in number_range if i % 2 == 0)
    return sum(even_numbers)
