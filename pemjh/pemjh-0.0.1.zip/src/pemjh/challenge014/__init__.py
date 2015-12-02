""" Challenge014 """


def get_chain_size(origin, known_chains):
    """ Find the length of the Collatz sequence starting with origin.
    >>> get_chain_size(13, {1: 1})
    10

    >>> known = dict()
    >>> answer = get_chain_size(13, known)
    >>> print answer, known
    10 {13: 10}

    >>> known = {1: 1}
    >>> answer = get_chain_size(13, known)
    >>> print answer, known
    10 {1: 1, 13: 10}
    """
    one_added = 1 not in known_chains
    if one_added:
        known_chains[1] = 1

    current = origin
    chain = 0

    while current not in known_chains:
        chain += 1
        if (current % 2) == 0:
            current /= 2
        else:
            current = 3 * current + 1

    # Add extra
    chain += known_chains[current]

    known_chains[origin] = chain

    if one_added:
        del known_chains[1]

    return chain


def challenge014():
    """ challenge014 """
    limit = 1000000

    chain = 0
    longest = 1
    known_chains = {1: 1}

    for i in xrange(1, limit):
        new_chain = get_chain_size(i, known_chains)
        if new_chain > chain:
            chain = new_chain
            longest = i

    return longest
