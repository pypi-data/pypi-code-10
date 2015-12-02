""" Challenge111 """
from pemjh.utilities.numbers import PrimeChecker


def isPrime(p, pc=PrimeChecker()):
    if p & 1:
        # Odd, ok
        # divisible by 5?
        if p % 5 == 0:
            return False
        else:
            return pc.isPrime(p)
    else:
        return False


def buildNums(repeated, other):
    if len(repeated) > 0:
        if len(repeated) > 1 or len(other) > 0:
            for b in buildNums(repeated[1:], other):
                yield [repeated[0]] + b
        else:
            yield [repeated[0]]

    if len(other) > 0:
        if len(repeated) > 0 or len(other) > 1:
            for b in buildNums(repeated, other[1:]):
                yield [other[0]] + b
        else:
            yield [other[0]]


def challenge111():
    """ challenge111 """
    M = [8, 9, 8, 9, 9, 9, 9, 9, 8, 9]
    N = []
    S = []

    for i in xrange(10):
        n = 0
        s = 0
        # use M[i] to build up all possible numbers
        for m in [list(("%0" + str(10 - M[i]) + "d") % m)
                  for m in xrange(0, 10**(10 - M[i]))]:
            if not any(int(c) == i for c in m):
                for b in [int("".join(b)) for b in buildNums([str(i)] * M[i],
                                                             m)]:
                    if b >= 10**(9):
                        # Check each for primality
                        if isPrime(b):
                            n += 1
                            s += b
        N.append(n)
        S.append(s)

    return sum(S)
