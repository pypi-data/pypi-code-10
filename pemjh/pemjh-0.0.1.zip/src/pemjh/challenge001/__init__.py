""" Challenge001 """


def challenge001():
    """ challenge001 """
    upper = 1000
    return sum(a for a in xrange(1, upper) if (a % 3 == 0) or (a % 5 == 0))
