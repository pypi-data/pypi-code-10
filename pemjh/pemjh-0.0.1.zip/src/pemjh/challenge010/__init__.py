""" Challenge010 """
from math import sqrt


def challenge010():
    """ challenge010 """
    limit = 2000000
    primes = [True] * limit
    for i in xrange(2, int(sqrt(limit)) + 1):
        if primes[i - 1]:
            for j in xrange(i**2 - 1, limit, i):
                primes[j] = False

    return sum(i + 1 for i, b in enumerate(primes) if b) - 1
