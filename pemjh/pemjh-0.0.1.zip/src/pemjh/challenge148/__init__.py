""" Challenge148 """


def get_biggest_triangle(row):
    current = row
    power = 0
    while 7 <= current:
        current //= 7
        power += 1

    return power


def get_non_7s(row):
    if row <= 7:
        return (row * (row + 1)) // 2

    # Get the biggest power 7 triangle
    big_triangle_power = get_biggest_triangle(row)

    # How many in the big triangle?
    big_triangle = 28**big_triangle_power

    # How many complete rows?
    complete_rows = row // (7**big_triangle_power)

    # How many extra rows?
    extra_rows = row % (7**big_triangle_power)

    # How many partial big triangles in the incomplete row?
    incomplete_triangles = complete_rows + 1

    return get_non_7s(complete_rows) * big_triangle + incomplete_triangles * \
        get_non_7s(extra_rows)


def challenge148():
    """ challenge148 """
    maximum = 1000000000

    return get_non_7s(maximum)
