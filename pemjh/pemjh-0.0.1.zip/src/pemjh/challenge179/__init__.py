""" Challenge179 """


def working(limit):
    # Make array for all numbers
    arr = [0] * (limit + 1)

    nSame = 0
    prev = 0
    for i in xrange(1, limit + 1):
        for a in xrange(i, limit + 1, i):
            arr[a] += 1

        curr = arr[i]
        if curr == prev:
            nSame += 1

        prev = curr

    return nSame


def challenge179():
    """ challenge179 """
    limit = 10**7
    return working(limit)
