""" Challenge015 """
from pemjh.utilities.numbers import fact


def get_routes(grid_size):
    """
    >>> get_routes(2)
    6
    """
    # Work out the row
    row = grid_size * 2
    # Get mid point of row
    midpoint = grid_size

    return fact(row) / (fact(midpoint)**2)


def challenge015():
    """ challenge015 """
    return get_routes(20)
