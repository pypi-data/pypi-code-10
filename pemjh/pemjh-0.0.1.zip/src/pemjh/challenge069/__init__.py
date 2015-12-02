""" Challenge069 """
from pemjh.utilities.numbers import sievedPrimes


def challenge069():
    """ challenge069 """
    limit = 1000000
    primes = list(sievedPrimes(limit))
    primes.remove(1)
    primes = dict([p, float(p) / (p - 1)] for p in primes)
    num_phi = [1.0] * limit
    for k, num in primes.items():
        current = k - 1
        while current < limit:
            num_phi[current] *= num
            current += k

    highest = max(num_phi)
    return num_phi.index(highest) + 1
