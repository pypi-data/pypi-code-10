""" Challenge066 """
from pemjh.utilities.numbers import rootConvergentGenerator

# Pell's equation


def is_square(num):
    """ Check if number is square """
    return int(num**0.5)**2 == num


def diophantine_x(num):
    """ Diophantine equation """
    for x_val, y_val in rootConvergentGenerator(num, True):
        ans = x_val**2 - num * y_val**2
        if ans == 1:
            return x_val


def challenge066():
    """ challenge066 """
    limit = 1000
    solutions = [[num, diophantine_x(num)] for num in xrange(1, limit + 1)
                 if not is_square(num)]
    return max(solutions, key=lambda x_val: x_val[1])[0]
