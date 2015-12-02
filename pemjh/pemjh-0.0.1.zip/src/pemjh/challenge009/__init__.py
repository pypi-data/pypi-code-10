""" Challenge009 """


def challenge009():
    """ challenge009 """
    # a2 + b2 - c2 = 0

    limit = 1000
    answer = 0

    # a_side can be 1 up to 1/3 away from limit
    for a_side in range(1, (limit / 3)):
        # b_side can be 1 more than a_side up to half the remainder
        remainder = limit - a_side
        for b_side in range((a_side + 1), (a_side + 1 + (remainder / 2))):
            c_side = limit - a_side - b_side
            if (a_side**2 + b_side**2 - c_side**2) == 0:
                answer = a_side * b_side * c_side

    return answer
