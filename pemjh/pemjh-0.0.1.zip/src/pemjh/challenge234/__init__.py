""" Challenge234 """
from pemjh.utilities.numbers import sievedPrimes


def myrange(low, high, step):
    current = low
    while current < high and step > 0 or current > high and step < 0:
        yield current
        current += step


def challenge234():
    """ challenge234 """
    # Get primes needed
    limit = 999966663333
    primes = sievedPrimes(1000000)

    primes.next()
    current = primes.next()

    total = list()

    for next in primes:

        # square of current will definitely not be semidivisable
        lows = set(myrange(current**2 + current,
                           next**2 if next**2 < limit + 1 else limit + 1,
                           current))

        highest = next**2 - next
        while highest > limit:
            highest -= next

        highs = set(myrange(highest, current**2, -next))

        # Get numbers in one or other but not both
        valid = lows.symmetric_difference(highs)

        total.extend(list(valid))

        current = next

    return sum(t for t in total if t < limit)
