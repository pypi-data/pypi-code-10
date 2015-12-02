""" Challenge116 """


def numVariations(blocks, tileSize, dec=True, known=dict()):
    if (blocks, tileSize) in known:
        return known[(blocks, tileSize)]
    nVariations = 0

    if blocks > 1:
        # work out with tile here
        if blocks >= tileSize:
            nVariations += numVariations(blocks - tileSize, tileSize, False)

        # work out with tile not here
        nVariations += numVariations(blocks - 1, tileSize, False)

    else:
        nVariations = 1

    if dec:
        nVariations -= 1

    known[(blocks, tileSize)] = nVariations

    return nVariations


def process(blocks):
    n2 = numVariations(blocks, 2)
    n3 = numVariations(blocks, 3)
    n4 = numVariations(blocks, 4)
    return n2 + n3 + n4


def challenge116():
    """ challenge116 """
    blocks = 50
    return process(blocks)
