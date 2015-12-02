""" Challenge049 """
import string
from pemjh.utilities.numbers import sievedPrimes


def challenge049():
    """ challenge049 """
    permutation_primes = dict()
    for prime in [n for n in sievedPrimes(9999) if n > 999]:
        chars = string.join(sorted(list(str(prime))), "")
        if chars in permutation_primes:
            permutation_primes[chars] += [prime]
        else:
            permutation_primes[chars] = [prime]

    # Remove those less than 2
    permutation_primes = dict([(c, p)
                               for c, p in permutation_primes.iteritems()
                               if len(p) > 2])

    del permutation_primes["1478"]

    for primes in permutation_primes.itervalues():
        for prime_1 in primes:
            for prime_2 in [p for p in primes if p != prime_1]:
                diff = prime_2 - prime_1
                prime_3 = prime_2 + diff
                if prime_3 in primes:
                    return int(str(prime_1) + str(prime_2) + str(prime_3))
