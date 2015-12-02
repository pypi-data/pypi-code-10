""" Challenge051 """
from itertools import cycle
from pemjh.utilities.numbers import PrimeChecker


def substitute_primes(template, substitute, checker):
    """
    >>> checker = PrimeChecker()
    >>> substitute_primes("13", "1", checker)
    (6, 13)
    >>> checker = PrimeChecker()
    >>> substitute_primes("56223", "2", checker)
    (7, 56003)
    """
    count = 0
    smallest = int(template)
    for i in xrange(0, 10):
        # Swap out the substitute for 0 - 9
        working = template.replace(substitute, str(i))
        # Check if prime
        if working[0] != "0":
            working = int(working)
            if checker.isPrime(int(working)):
                if working < smallest:
                    smallest = working
                count += 1

    return count, smallest


def has_3_same_digits(i):
    """
    >>> has_3_same_digits(1234)
    False
    >>> has_3_same_digits(111)
    True
    >>> has_3_same_digits(232523)
    True
    >>> has_3_same_digits(121212)
    True
    >>> has_3_same_digits(122223)
    False
    >>> has_3_same_digits(1212121)
    True
    """
    word = str(i)
    return any(word.count(d) == 3 for d in set(word))


def challenge051():
    """ challenge051 """
    prime_checker = PrimeChecker()
    step = cycle([2, 4])
    current = 5
    while True:
        # Check current
        if prime_checker.isPrime(current) and has_3_same_digits(current):
            # Substitute 0 to 9
            word = str(current)
            for i in xrange(0, 10):
                number_of_primes, smallest = substitute_primes(word,
                                                               str(i),
                                                               prime_checker)
                if number_of_primes == 8:
                    return smallest

        current += step.next()
