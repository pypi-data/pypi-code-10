""" Challenge027 """
from pemjh.utilities.numbers import sievedPrimes, isPrime


def challenge027():
    """ challenge027 """
    limit = 999

    maximum_a = 0
    maximum_b = 0

    maximum = 1
    primes = list(sievedPrimes(limit + 1))
    for prime in primes:
        for a_side in xrange(-prime, limit + 1):
            root = 1
            while True:
                potential_prime = root * (root + a_side) + prime
                if not isPrime(potential_prime):
                    break
                root += 1

            if root > maximum:
                maximum = root
                maximum_a = a_side
                maximum_b = prime

    return maximum_a * maximum_b
