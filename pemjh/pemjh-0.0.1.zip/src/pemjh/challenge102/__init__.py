""" Challenge102 """
from __future__ import with_statement
from os.path import dirname, abspath


def enclosesOrigin(x1, y1, x2, y2, x3, y3):
    # To enclose, 1 point should be left (or right) of 0
    # 0 should be between the two lines joining this point with the other 2

    # Remove invalid cases
    x12 = x1 * x2
    x23 = x2 * x3
    x31 = x3 * x1
    if not (x12 > 0 and x23 > 0 and x31 > 0):
        # Points cross the divide
        # Find the differing point
        if x12 * x23 > 0:
            # x2 is on the other side
            i1 = getYIntercept(x2, y2, x1, y1)
            i2 = getYIntercept(x2, y2, x3, y3)
        elif x23 * x31 > 0:
            # x3 is on the other side
            i1 = getYIntercept(x3, y3, x1, y1)
            i2 = getYIntercept(x3, y3, x2, y2)
        else:
            # x1 is on the other side
            i1 = getYIntercept(x1, y1, x2, y2)
            i2 = getYIntercept(x1, y1, x3, y3)

        if i1 * i2 < 0:
            return True

    return False


def getYIntercept(x1, y1, x2, y2):
    # Assume there is a run
    m = (y2 - y1) / (x2 - x1)
    # y1 = mx1 + c
    # c = y1 - mx1
    c = y1 - m * x1

    # Return y for x = 0
    return c


def challenge102():
    """ challenge102 """
    path = "%s/triangles.txt" % dirname(abspath(__file__))
    nEnclosing = 0
    with open(path) as f:
        for l in [l.strip().split(",") for l in f]:
            ax, ay, bx, by, cx, cy = [float(i) for i in l]
            if enclosesOrigin(ax, ay, bx, by, cx, cy):
                nEnclosing += 1

    return nEnclosing
