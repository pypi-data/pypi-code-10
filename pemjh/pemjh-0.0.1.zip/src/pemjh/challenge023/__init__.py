""" Challenge023 """


def sum_of_divisors(number):
    """
    >>> sum_of_divisors(28)
    56
    >>> sum_of_divisors(12)
    28
    """

    prod = 1

    k = 2
    while k*k <= number:
        prime_factor_sum = 1
        while (number % k) == 0:
            prime_factor_sum = prime_factor_sum * k + 1
            number /= k
        prod *= prime_factor_sum
        k += 1

    if number > 1:
        prod *= (1 + number)

    return prod


def is_sum(i, abundants):
    """
    >>> is_sum(24, [12])
    True
    >>> is_sum(25, [12])
    False
    >>> is_sum(7, [3, 4])
    True
    """
    return any(i - a in abundants for a in abundants)


def challenge023():
    """ challenge023 """
    abundants = set(i for i in xrange(1, 28124)
                    if sum_of_divisors(i) > (i * 2))

    return sum(i for i in xrange(1, 28124) if not is_sum(i, abundants))
