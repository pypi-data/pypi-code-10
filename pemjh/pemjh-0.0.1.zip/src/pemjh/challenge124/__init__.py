""" Challenge124 """
from pemjh.utilities.numbers import sievedPrimes


def sort124(a, b):
    if a[0] > b[0] or \
       (a[0] == b[0] and a[1] > b[1]):

        return 1

    if a[0] == b[0] and a[1] == b[1]:
        return 0

    if a[0] < b[0] or \
       (a[0] == b[0] and a[1] < b[1]):

        return -1


def challenge124():
    """ challenge124 """
    limit = 100000
    lookup = 10000

    # Setup array of 1s
    numbers = [1] * limit

    # Get primes needed
    # Multiply each by the primes
    for p in sievedPrimes(limit + 1):
        for i in xrange(p - 1, limit, p):
            numbers[i] *= p

    # enumerate the list
    numbers = [[rad, n + 1] for n, rad in enumerate(numbers)]

    # Sort by rec then n
    numbers.sort(sort124)

    # Get lookup

    return numbers[lookup - 1][1]
