""" Challenge162 """


def challenge162():
    """ challenge162 """
    total = sum(15 * 16**(n - 1) + 41 * 14**(n - 1) - (43 * 15**(n - 1) +
                                                       13**n)
                for n in xrange(3, 17))

    return hex(total).upper()[2: -1]
