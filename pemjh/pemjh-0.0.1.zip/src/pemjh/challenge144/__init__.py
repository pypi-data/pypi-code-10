""" Challenge144 """
from math import atan2, tan


def solveQuadratic(a, b, c):
    sqPart = b**2 - (4 * a * c)
    return (-b + sqPart**0.5) / (2 * a), (-b - sqPart**0.5) / (2 * a)


def reflect(x, y, gradient):
    # Get gradient at impact point
    impGrad = -4 * x / y

    # Get impact angle
    impAngle = atan2(impGrad, 1)

    # Get incoming angle
    inAngle = atan2(gradient, 1)

    # Get difference
    diffAngle = inAngle - impAngle

    # Get new angle
    newAngle = impAngle - diffAngle

    # Convert new angle to gradient
    newGradient = tan(newAngle)

    # Return new gradient
    return newGradient


def nextStep(start):
    # y = sqrt(100 - 4x**2)
    m = start[1]
    # y = mx + c
    # c = y - mx
    c = start[0][1] - m * start[0][0]

    # mx + c = sqrt(100 - 4x**2)
    # (mx + c)**2 = 100 - 4x**2
    # (mx)**2 + 2cmx + c**2 = 100 - 4x**2
    # (m**2)(x**2) + 4x**2 + 2cmx + c**2 - 100 = 0
    # (m**2 + 4)(x**2) + 2cmx + (c**2 - 100) = 0
    x1, x2 = solveQuadratic(m**2 + 4, 2 * c * m, c**2 - 100)

    # Get the impact point
    if abs(x1 - start[0][0]) < abs(x2 - start[0][0]):
        xImpact = x2
    else:
        xImpact = x1

    yImpact = m * xImpact + c

    return ((xImpact, yImpact), reflect(xImpact, yImpact, m))


def exiting(point):
    return point[0] >= -0.01 and point[0] <= 0.01 and point[1] > 0


def challenge144():
    """ challenge144 """
    current = ((0, 10.1), -19.7 / 1.4)
    # Move to next
    current = nextStep(current)

    count = 0

    while not exiting(current[0]):
        current = nextStep(current)
        count += 1

    return count
