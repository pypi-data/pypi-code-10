""" Challenge021 """
from pemjh.utilities.numbers import divisors


def challenge021():
    """ challenge021 """
    maximum = 10000
    total = 0
    known_divisors = {}
    for number in xrange(1, maximum):
        # Get the divisors total
        sum_of_divisors = 0
        for divisor in divisors(number, False):
            sum_of_divisors += divisor

        if number != sum_of_divisors:
            # Is the number already defined?
            if sum_of_divisors in known_divisors:
                if known_divisors[sum_of_divisors] == number:
                    # Add the pair
                    total += number + sum_of_divisors

        # Add the sum to the dictionary
        known_divisors[number] = sum_of_divisors

    return total
