""" Challenge067 """
from os.path import dirname, abspath
from pemjh.utilities.numbers import getTriangleRouteLength


def challenge067():
    """ challenge067 """
    rows = []
    # Read in the file
    with open("%s/triangle.txt" % dirname(abspath(__file__))) as triangle_file:
        for line in triangle_file:
            # Create a row
            vals = [int(x) for x in line.split()]
            rows.append(vals)
    return getTriangleRouteLength(rows)
