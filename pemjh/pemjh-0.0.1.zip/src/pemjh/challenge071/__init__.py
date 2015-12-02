""" Challenge071 """
from math import floor, ceil


def challenge071():
    """ challenge071 """
    target_numerator = 3
    target_denominator = 7
    target = float(target_numerator) / target_denominator
    limit = 1000000
    best_numerator = 0
    best_denominator = 1
    best = 0
    for den in xrange(limit, 1, -1):
        # Get Numerator range
        high_numerator = int(floor(den * target))
        low_numerator = int(ceil(den * best))
        for num in xrange(high_numerator, low_numerator - 1, -1):

            if num % target_numerator == 0 and den % target_denominator == 0:
                if num / target_numerator == den / target_denominator:
                    continue

            left_side = num * best_denominator
            right_side = best_numerator * den
            if left_side > right_side:
                best_numerator, best_denominator = num, den
                best = float(best_numerator) / best_denominator
                break

    return best_numerator
