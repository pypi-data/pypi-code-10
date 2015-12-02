""" Challenge045 """


def pentagonal(i):
    """
    >>> pentagonal(1)
    1
    >>> pentagonal(5)
    35
    """
    return i * (3 * i - 1) / 2


def hexagonal(i):
    """
    >>> hexagonal(1)
    1
    >>> hexagonal(5)
    45
    """
    return i * (2 * i - 1)


def pentagonal_and_hexagonal():
    """
    >>> from itertools import islice
    >>> list(islice(pentagonal_and_hexagonal(), 3))
    [1, 40755, 1533776805L]
    """
    # No need to find triangle, since all hex are tri
    pent_n = 1
    hex_n = 1
    while True:
        p_value = pentagonal(pent_n)
        h_value = hexagonal(hex_n)

        if p_value == h_value:
            yield p_value

        if p_value < h_value:
            pent_n += 1
        else:
            hex_n += 1


def challenge045():
    """ challenge045 """
    from itertools import dropwhile
    return dropwhile(lambda x: x <= 40755, pentagonal_and_hexagonal()).next()
