""" Challenge127 """
from pemjh.utilities.numbers import gcd, sievedPrimes


def challenge127():
    """ challenge127 """
    maximum = 120000

    primes = list(sievedPrimes(maximum))

    rads = [1, ] * maximum

    for prime in primes[1:]:
        for i in xrange(prime - 1, maximum, prime):
            rads[i] *= prime

    rad_lookup = [[r, i + 1] for i, r in enumerate(rads)]

    rad_lookup.sort()

    result = 0
    for c in xrange(1, maximum + 1):
        for next in rad_lookup:
            a = next[1]
            if next[0] * rads[c - 1] >= c:
                break
            b = c - a

            if a < (c / 2) and next[0] * rads[b - 1] * rads[c - 1] < c and \
                    gcd(a, b) == 1:
                result += c

    return result
