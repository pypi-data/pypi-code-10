""" Challenge031 """


def get_pattern_count(left, coins):
    """ Find the amount of ways to make "left" using the remaining coins.
    Pennies are included by default.
    >>> get_pattern_count(10, (2, 5, 10))
    11
    """
    if len(coins) == 0:
        return 1
    # Get next coin
    coin = coins[0]
    # See how many could go into left
    most = left // coin
    # Loop through possible
    count = 0
    for i in xrange(0, most + 1):
        remaining = left - i * coin
        count += get_pattern_count(remaining, coins[1:])

    return count


def challenge031():
    """ challenge031 """
    return get_pattern_count(200, [200, 100, 50, 20, 10, 5, 2])
