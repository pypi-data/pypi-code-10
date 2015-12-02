""" Challenge250 """


def slow_way(limit):
    values = [0] * 250
    for i in xrange(1, limit):
        total = int(pow(i, i, 250))
        values[total] += 1

    mods = [1] + [0] * 249

    # Loop through each mod found
    for i in xrange(250):
        # Loop through each instance of the modulus
        for _ in xrange(values[i]):
            # Apply the modulus to all already found modulii
            # Each space is the number of itself, + the number that can become
            # it
            mods = [(mods[k] + mods[(k - i) % 250]) % 10**16
                    for k in xrange(250)]

    # Return the number of 0s
    return mods[0] - 1


def challenge250():
    """ challenge250 """
    limit = 250251
    return slow_way(limit)
