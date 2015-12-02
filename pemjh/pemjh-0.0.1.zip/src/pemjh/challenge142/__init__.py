""" Challenge142 """


def perfectSquare(n):
    return (int(n ** 0.5))**2 == n


def valid(a, b):
    return perfectSquare(a + b) and perfectSquare(a - b)


def challenge142():
    """ challenge142 """
    n_squares = 1000

    squares = [n**2 for n in xrange(n_squares)]

    highest = dict()

    # Find pairs of values
    for upper_index in xrange(n_squares):
        for lower_index in xrange(upper_index - 2, 0, -2):
            upper = (squares[upper_index] + squares[lower_index]) // 2
            lower = (squares[upper_index] - squares[lower_index]) // 2

            if upper in highest:
                highest[upper].append(lower)
            else:
                highest[upper] = [lower]

    # Find triples
    for high, lows in highest.iteritems():
        if len(lows) > 1:
            # Sort highest to low
            matches = list(reversed(sorted(set(lows))))
            for first in matches[:-1]:
                if first in highest:
                    intersect = set(highest[first]).intersection(
                        set(matches[matches.index(first) + 1:]))
                    if len(intersect) > 0:
                        return high + first + list(intersect)[0]
