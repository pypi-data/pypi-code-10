""" Challenge204 """
from pemjh.utilities.numbers import sievedPrimes


def getHams(current, limit, primes):
    nCount = 0
    for p in primes:
        # Multiply current by p until limit is hit
        pCurrent = current * p
        if pCurrent > limit:
            # all following will breach too
            break

        while pCurrent <= limit:
            nCount += 1
            nCount += getHams(pCurrent, limit, primes[primes.index(p) + 1:])
            pCurrent *= p

    return nCount


def hamNums(maxPrime, limit):
    # generate primes without 1
    primes = list(sievedPrimes(maxPrime))[1:]

    return getHams(1, limit, primes) + 1


def challenge204():
    """ challenge204 """
    return hamNums(100, 10**9)
