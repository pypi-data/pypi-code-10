""" Challenge028 """


def challenge028():
    """ challenge028 """
    size = 1001
    layers = (size + 1) // 2

    current = 1
    total = 1
    # Cycle through layers
    for i in xrange(2, layers + 1):
        sidestep = (i * 2) - 2
        total += (current * 4) + (sidestep * 10)
        current += (sidestep * 4)

    return total
