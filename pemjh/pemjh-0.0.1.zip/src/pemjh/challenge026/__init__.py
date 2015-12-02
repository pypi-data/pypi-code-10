""" Challenge026 """


def challenge026():
    """ challenge026 """
    biggest = 0
    biggest_denominator = 0
    for denominator in xrange(1, 1000):
        numerator = 1
        numerators = []
        while numerators.count(numerator) == 0:
            numerators.append(numerator)
            numerator = ((numerator * 10) % denominator)

        if numerator > 0:
            cycle_length = len(numerators) - numerators.index(numerator)
            if cycle_length > biggest:
                biggest = cycle_length
                biggest_denominator = denominator
        else:
            cycle_length = 0

    return biggest_denominator
