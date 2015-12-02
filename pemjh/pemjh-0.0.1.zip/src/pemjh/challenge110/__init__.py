""" Challenge110 """
from pemjh.utilities.numbers import sievedPrimes, primeIndices


def challenge110():
    """ challenge110 """
    target = 4000000
    primeLimit = 10000

    primes = list(sievedPrimes(primeLimit))[1:]

    # Get suitable primeIndices
    indices = primeIndices((target * 2 - 1), 0, primes, 0)

    return indices
