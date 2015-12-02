""" Challenge034 """
from pemjh.utilities.numbers import fact


def challenge034():
    """ challenge034 """
    limit = 2540160
    facts = dict((str(i), fact(i)) for i in xrange(0, 10))

    found = []
    for i in xrange(3, limit + 1):
        factorial_total = 0
        for digits in str(i):
            factorial_total += facts[digits]
        if factorial_total == i:
            found.append(i)
    return sum(found)
