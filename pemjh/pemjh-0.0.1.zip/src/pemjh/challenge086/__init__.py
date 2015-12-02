""" Challenge086 """


def is_int(a, msq, square_library):
    return a**2 + msq in square_library


def get_num_pairs(pair_sum, limit):

    num_pairs = 0

    a = 0
    b = pair_sum
    while True:
        a += 1
        b -= 1
        if a > b:
            break
        if b <= limit:
            num_pairs += 1
    return num_pairs


def get_step_size(m, square_library):
    msq = m**2
    return sum(get_num_pairs(a, m) for a in range(2, (2 * m) + 1)
               if is_int(a, msq, square_library))


def challenge086():
    """ challenge086 """
    limit = 1000000

    square_limit = 4000
    squares = set(x*x for x in xrange(square_limit))

    m = 0
    current = 0
    while current < limit:
        m += 1
        current += get_step_size(m, squares)

    return m
