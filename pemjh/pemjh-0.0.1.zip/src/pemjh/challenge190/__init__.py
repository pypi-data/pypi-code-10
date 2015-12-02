""" Challenge190 """


def P(m):
    return int(reduce(lambda a, b: a * b,
                      [(j * 2.0/(m + 1))**j for j in range(1, m + 1)]))


def challenge190():
    """ challenge190 """
    return sum(P(m) for m in xrange(2, 16))
