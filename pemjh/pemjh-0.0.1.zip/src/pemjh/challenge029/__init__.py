""" Challenge029 """


def challenge029():
    """ challenge029 """
    a_lower = 2
    a_upper = 100
    b_lower = 2
    b_upper = 100

    nums = set([])
    for current_a in xrange(a_lower, a_upper + 1):
        for current_b in xrange(b_lower, b_upper + 1):
            nums.add(current_a**current_b)

    return len(nums)
