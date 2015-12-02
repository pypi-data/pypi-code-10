""" Challenge006 """


def challenge006():
    """ challenge006 """
    limit = 100

    sum_of_squares = 0
    # Find the sum of the squares
    for i in range(1, limit + 1):
        sum_of_squares += i**2

    # Find the sum
    total = (limit * (limit + 1)) / 2

    # Find the square
    square_of_sums = total**2

    # Find the difference
    difference = abs(square_of_sums - sum_of_squares)

    return difference
