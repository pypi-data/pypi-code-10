""" Challenge048 """


def challenge048():
    """ challenge048 """
    limit = 1000
    return sum([i**i for i in xrange(1, limit + 1)]) % 10000000000
