""" Challenge108 """
from pemjh.utilities.numbers import sievedPrimes, primeIndices


def challenge108():
    """ challenge108 """
    target = 1000
    primeLimit = 10000

    primes = list(sievedPrimes(primeLimit))[1:]

    # Get suitable primeIndices
    indices = primeIndices((target * 2 - 1), 0, primes, 0)

    return indices
