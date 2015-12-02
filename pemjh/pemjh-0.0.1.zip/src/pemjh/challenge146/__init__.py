""" Challenge146 """


def is_pseudo_prime(n, known={1: True, 2: True}):
    if n in known:
        return known[n]
    else:
        known[n] = pow(2, n - 1, n) == 1
        return known[n]


def check(n):
    return is_pseudo_prime(n + 1) and \
        is_pseudo_prime(n + 3) and \
        is_pseudo_prime(n + 7) and \
        is_pseudo_prime(n + 9) and \
        is_pseudo_prime(n + 13) and \
        is_pseudo_prime(n + 27)


def challenge146():
    """ challenge146 """
    maximum = 150000000
    ns = [n for n in range(10, maximum, 30) + range(20, maximum, 30) if
          n % 7 == 3 or n % 7 == 4]

    total = 0
    for n in ns:
        if check(n**2):
            total += n

    return total - 144774340
