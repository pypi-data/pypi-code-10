""" Challenge174 """


def getNumEvenDivisors(n, known=dict()):
    if n in known:
        return known[n]

    nDiv = 0

    two = 2
    while two**2 < n:
        if n % (two * 2) == 0:
            nDiv += 1

        two += 2

    return nDiv


def challenge174():
    """ challenge174 """
    limit = 1000000

    nSquares = [getNumEvenDivisors(i) for i in xrange(4, limit + 1, 4)]

    nMatches = 0
    for n in xrange(1, 10 + 1):
        nMatches += len([x for x in nSquares if x == n])

    return nMatches
