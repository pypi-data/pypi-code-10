""" Challenge100 """


def challenge100():
    """ challenge100 """
    b = 85
    n = 120
    while n < 10**12:
        b, n = 3*b + 2*n - 2, 4*b + 3*n - 3
    return b
