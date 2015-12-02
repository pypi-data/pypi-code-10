""" Challenge076 """


def get_num_break_downs(num, last, known):
    """ Get the number of break downs """
    if num in known:
        if last in known[num]:
            return known[num][last]
    else:
        known[num] = dict()

    num_break_downs = 0
    for next_num in xrange(last if last <= num else num, 0, -1):
        left = num - next_num
        if left == 0:
            num_break_downs += 1
        else:
            num_break_downs += get_num_break_downs(left, next_num, known)

    known[num][last] = num_break_downs
    return num_break_downs


def challenge076():
    """ challenge076 """
    # 2: 1
    # 3: 2
    # 4: 4
    # 5: 6
    # 6: 10
    # 7: 14
    # 8: 21
    # 9: 29
    # 10: 41

    target = 100
    known = dict()
    return get_num_break_downs(target, target - 1, known)
