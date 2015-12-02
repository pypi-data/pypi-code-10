""" Challenge058 """
from pemjh.utilities.numbers import PrimeChecker


def challenge058():
    """ challenge058 """
    current = 1
    prime_count = 0
    diagonals = 1

    prime_checker = PrimeChecker()

    # Cycle through layers
    sidestep = 2
    while True:
        for _ in xrange(1, 4):
            current += sidestep

            if prime_checker.isPrime(current):
                prime_count += 1

        current += sidestep

        diagonals += 4

        if prime_count * 10 < diagonals:
            return sidestep + 1

        sidestep += 2
