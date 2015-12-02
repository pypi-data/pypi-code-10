""" Challenge057 """


def challenge057():
    """ challenge057 """
    count_top_heavy = 0

    for expansions in xrange(1, 1001):
        numerator = 2
        denominator = 1
        for _ in xrange(1, expansions):
            numerator, denominator = 2 * numerator + denominator, numerator

        numerator, denominator = numerator + denominator, numerator

        if len(str(numerator)) > len(str(denominator)):
            count_top_heavy += 1

    return count_top_heavy
