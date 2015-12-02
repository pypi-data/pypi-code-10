""" Challenge115 """


def numVariations(blocks, minimum, tileSizes, known=dict()):
    if (blocks, minimum) in known:
        return known[(blocks, minimum)]
    nVariations = 0

    if blocks > 1:
        for tileSize in tileSizes:
            if tileSize > blocks:
                break

            # Always an extra 1 block length for the spacer
            left = blocks - tileSize - 1
            if left < 0:
                left = 0
            nVariations += numVariations(left, minimum, tileSizes)

        # work out with no tile here
        nVariations += numVariations(blocks - 1, minimum, tileSizes)

    else:
        nVariations = 1

    known[(blocks, minimum)] = nVariations

    return nVariations


def f(minimum, blocks):
    n = numVariations(blocks, minimum, range(minimum, blocks + 1))
    return n


def challenge115():
    """ challenge115 """
    minimum = 50
    b = 2
    while 1:
        ans = f(minimum, b)
        if ans > 1000000:
            return b
        b += 1
