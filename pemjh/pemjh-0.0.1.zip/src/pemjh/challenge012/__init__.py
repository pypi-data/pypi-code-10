""" Challenge012 """
from pemjh.utilities.numbers import getNumDivisorsHelped


def triangle_divisors():
    """ Generate the number of divisors of each triangle number.
    >>> import itertools
    >>> list(itertools.islice(triangle_divisors(), 0, 10))
    [1, 2, 4, 4, 4, 4, 6, 9, 6, 4]
    """
    number = 1
    odd_divisors = 1
    even_divisors = 1
    known_divisors = {}
    while True:
        # Get unknown divisors
        if number % 2 == 0:
            # number is even, reset odd
            odd_divisors = getNumDivisorsHelped(number + 1, known_divisors)
        else:
            # number is odd, reset even
            even_divisors = getNumDivisorsHelped((number + 1) / 2,
                                                 known_divisors)
        yield odd_divisors * even_divisors
        number += 1


def challenge012():
    """ challenge012 """
    limit = 500
    triangle_root = 1
    divisors = triangle_divisors()
    while divisors.next() <= limit:
        triangle_root += 1

    return (triangle_root * (triangle_root + 1)) / 2
