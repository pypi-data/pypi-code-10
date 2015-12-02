""" Challenge135 """


def getNumTarget(limit, target):
    possible = [0] * limit
    for x in xrange(1, limit):
        # x * (x / 4 + 1)
        # x**2 / 4 + x = limit
        # x**2 + 4x = 4limit
        # x**2 + 4x - 4limit = 0
        for n in xrange(x / 4 + 1, x):
            n = x * (4 * n - x)
            if n >= limit:
                break

            if n > 0:
                possible[n] += 1

    return possible.count(target)


def challenge135():
    """ challenge135 """
    return getNumTarget(1000000, 10)
