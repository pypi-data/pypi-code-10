""" Challenge064 """
from pemjh.utilities.numbers import continueGenerator


def challenge064():
    """ challenge064 """
    limit = 10000

    odd_count = 0
    for num in [num for num in xrange(2, limit + 1)
                if int(num**0.5) != num**0.5]:

        length = len(list(continueGenerator(num))) - 1

        if length & 1:
            odd_count += 1

    return odd_count
