""" Challenge073 """
from math import ceil, floor


def challenge073():
    """ challenge073 """
    limit = 10000
    upper_numerator = 1.0
    upper_denominator = 2.0
    lower_numerator = 1.0
    lower_denominator = 3.0

    fractions = set()
    for den in xrange(5, limit + 1):
        lower_limit = lower_numerator * den / lower_denominator
        lower_limit = int(lower_limit + 1 if lower_limit % 1 == 0 else
                          ceil(lower_limit))
        upper_limit = upper_numerator * den / upper_denominator
        upper_limit = int(upper_limit - 1 if upper_limit % 1 == 0 else
                          floor(upper_limit))

        for num in xrange(lower_limit, upper_limit + 1):
            # Check that num, den don't share factors
            fractions.add(float(num) / den)

    return len(fractions)
