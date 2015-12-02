""" Challenge035 """
from math import sqrt


def circulars(number):
    """
    >>> list(circulars(136))
    [361, 613, 136]
    """
    characters = str(number)
    if characters.count("0") > 0:
        print characters

    for i in xrange(1, len(characters) + 1):
        # String from i to end, start to i
        next_string = "%s%s" % (characters[i:], characters[:i])
        yield int(next_string)


def challenge035():
    """ challenge035 """
    limit = 1000000
    primes = [True] * (limit)
    primes[0] = False
    primes[1] = False

    for i in xrange(2, int(sqrt(limit)) + 1):
        if primes[i]:
            for j in xrange(i**2, limit, i):
                primes[j] = False

    disallowed_characters = ["0", "2", "4", "6", "8", "5"]
    # For each in orderedPrimes, remove if any circulars are missing
    primes = set([p for p, b in enumerate(primes)
                  if b and ((p < 10) or
                            not any(c in str(p)
                                    for c in disallowed_characters))])

    circular_count = 0

    while len(primes) > 0:
        # Get all circulars for the next prime
        circular_list = set(circulars(iter(primes).next()))

        # Remove all that can be found, if all found then add to count
        all_found = True
        for circular in circular_list:
            if circular in primes:
                primes.remove(circular)
            else:
                # Missing
                all_found = False

        if all_found:
            circular_count += len(circular_list)

    return circular_count
