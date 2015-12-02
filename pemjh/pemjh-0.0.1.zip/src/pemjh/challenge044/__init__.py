""" Challenge044 """
from math import sqrt


def pent(i):
    """
    >>> pent(1)
    1
    >>> pent(10)
    145
    """
    return i * (3 * i - 1) / 2


def is_pent(potential):
    """
    >>> is_pent(92)
    True
    >>> is_pent(48)
    False
    """
    return max((1.0 + sqrt(1.0 + 24.0 * potential)) / 6.0,
               (1.0 - sqrt(1.0 + 24.0 * potential)) / 6.0) % 1 == 0


def challenge044():
    """ challenge044 """
    diff = 0
    k = 2
    while diff == 0:
        pent_k = pent(k)
        # Search back to find any valid values
        performed_one_step = False
        for pent_j in [pent(j) for j in xrange(k, 0, -1)]:
            diff_pk_pj = pent_k - pent_j
            if diff > 0 and diff < diff_pk_pj:
                break
            if is_pent(pent_j + pent_k) and is_pent(diff_pk_pj):
                diff = diff_pk_pj
            performed_one_step = True
        k += 1
        if not performed_one_step:
            break

    return diff
