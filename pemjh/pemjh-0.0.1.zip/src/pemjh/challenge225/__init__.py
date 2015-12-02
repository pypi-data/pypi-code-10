""" Challenge225 """


def challenge225():
    """ challenge225 """
    # Prime factors cycle, wait until back to 1, 1, 1 and there is no answer,
    # else the answer has been found

    odds = []
    current = 27
    while len(odds) != 124:

        a, b, c = 1, 1, 3
        while c > 0 and a * b * c != 1:
            a, b, c = b, c, (a + b + c) % current
        if c == 1:
            odds.append(current)
        current += 2
    return odds[-1]
