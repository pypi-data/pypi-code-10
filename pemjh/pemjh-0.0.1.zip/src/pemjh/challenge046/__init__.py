""" Challenge046 """
from math import sqrt
from pemjh.utilities.numbers import isPrime


def has_criteria(potential):
    """
    >>> has_criteria(9)
    True
    >>> has_criteria(5777)
    False
    """
    limit = int(sqrt(potential // 2))
    for square_doubled in [2 * i**2 for i in xrange(limit, 0, -1)]:
        diff = potential - square_doubled
        if diff == 1 or isPrime(diff):
            return True

    return False


def challenge046():
    """ challenge046 """
    odd_composite = 3
    while True:

        # Find doubled squares lower than odd_composite
        if not has_criteria(odd_composite):
            return odd_composite

        odd_composite += 2
        while odd_composite == 1 or isPrime(odd_composite):
            odd_composite += 2
