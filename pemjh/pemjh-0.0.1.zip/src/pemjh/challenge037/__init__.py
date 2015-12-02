""" Challenge037 """
from pemjh.utilities.numbers import isPrime


def is_truncated_prime(potential):
    """
    >>> is_truncated_prime(3797)
    True
    >>> is_truncated_prime(3798)
    False
    """
    divisor = 1
    # Check first digit is prime
    while True:
        trunc = potential // divisor
        if trunc <= 0:
            break
        if trunc == 1 or not isPrime(trunc):
            return False
        divisor *= 10

    while (potential % divisor) > 0:
        trunc = potential % divisor
        if trunc == 1 or not isPrime(potential % divisor):
            return False
        divisor /= 10

    return True


def challenge037():
    """ challenge037 """
    potential = 23
    found = []
    while len(found) < 11:
        if is_truncated_prime(potential):
            found.append(potential)
        potential += 2

    return sum(found)
