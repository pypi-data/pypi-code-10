""" Challenge164 """


def numLosses(size, previousThree, useZero, known=dict()):

    key = (size, previousThree, useZero)

    if key in known:
        return known[key]

    nVariations = 0

    if sum(previousThree) > 9:
        # Completed
        nVariations += 10**size

    elif size > 0:

        for next in xrange(0 if useZero else 1, 10):
            nVariations += numLosses(size - 1,
                                     (previousThree[1],
                                      previousThree[2],
                                      next),
                                     True)

    known[key] = nVariations

    return nVariations


def challenge164():
    """ challenge164 """
    size = 20
    possible = 10**(size - 1) * 9
    nLosses = numLosses(size, (0, 0, 0), False)

    return possible - nLosses
