""" Challenge047 """


def challenge047():
    """ challenge047 """
    limit = 1000000

    factors = [1, 1] + [0] * (limit - 1)

    count = 0
    for potential_answer in xrange(2, limit):
        if factors[potential_answer] == 0:
            # prime
            count = 0
            for multiple in xrange(potential_answer, limit, potential_answer):
                factors[multiple] += 1
        elif factors[potential_answer] == 4:
            # Found one
            count += 1
            if count == 4:
                return potential_answer - 3
        else:
            count = 0
