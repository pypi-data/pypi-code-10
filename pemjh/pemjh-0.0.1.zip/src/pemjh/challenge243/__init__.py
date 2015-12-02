""" Challenge243 """
from pemjh.utilities.numbers import sievedPrimes


def prime_factors(number, primes):
    for prime in primes:
        if number % prime == 0:
            yield prime


def phi(number, primes):
    small_factor = number
    for factor in prime_factors(number, primes):
        number = int((number * factor - number) // factor)
        small_factor = number if number < small_factor else small_factor
    return number


def challenge243():
    """ challenge243 """
    test_val = float(15499) / float(94744)
    minimum = 1.0

    primes = list(sievedPrimes(30))[1:]

    # 2, 4, 6, 10, 12, 16, 18
    d = 1
    for prime in sievedPrimes(30):
        if prime == 1:
            continue

        d *= prime

        ratio = float(phi(d, primes)) / float(d - 1)

        if ratio < minimum:
            minimum = ratio

            if ratio < test_val:
                # Gone over, move back to previous and then try multiples
                found = d / prime

                for m in xrange(2, 5):
                    d = found * m
                    ratio = float(phi(d, primes)) / float(d - 1)

                    if ratio < test_val:
                        return d

    return "Don't know"
