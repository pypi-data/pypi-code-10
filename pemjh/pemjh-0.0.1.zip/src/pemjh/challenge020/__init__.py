""" Challenge020 """


def factorial(root):
    """
    >>> factorial(10)
    3628800
    """
    total = 1
    for i in xrange(1, root + 1):
        total *= i
    return total


def challenge020():
    """ challenge020 """
    # Get factorial
    fact = factorial(100)
    # Set as string
    fact = str(fact)
    # Total up the numbers
    total = 0
    for digit in fact:
        total += int(digit)
    return total
