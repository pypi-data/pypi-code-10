""" Challenge091 """


def bruteForce(n):
    nTriangles = 0

    # Loop through each point as the right angle
    for x1 in xrange(0, n + 1):
        for y1 in xrange(0, n + 1):
            if x1 == 0 and y1 == 0:
                # Special case of origin
                nTriangles += n**2
            elif x1 == 0 or y1 == 0:
                # Special case
                nTriangles += n
            else:
                # Loop through other points
                for x2 in xrange(0, n + 1):
                    for y2 in xrange(0, n + 1):
                        if x2 == 0 and y2 == 0:
                            # cannot be origin
                            pass
                        if x1 == x2 and y1 == y2:
                            # cannot be same as right angle
                            pass
                        else:
                            # change:
                            # (y2 - y1) / (x2 - x1)
                            # y1 / x1 == - (x2 - x1) / (y2 - y1)
                            # y1 (y2 - y1) == -x1 (x2 - x1)
                            if y1 * (y2 - y1) == x1 * (x1 - x2):
                                nTriangles += 1
    return nTriangles


def challenge091():
    """ challenge091 """
    gridSize = 50

    return bruteForce(gridSize)
