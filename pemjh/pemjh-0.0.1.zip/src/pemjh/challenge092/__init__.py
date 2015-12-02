""" Challenge092 """
from pemjh.utilities.numbers import fact


def numbers(current, start, end, digits):
    if digits == 0:
        yield current
        return
    elif digits == 1 and start == 0:
        start = 1

    # Build the number,
    for i in xrange(start, end):
        for j in numbers(current + [i], i, end, digits - 1):
            yield j


def permutations(digits):
    prevI = -1
    nI = 0
    quantities = fact(len(digits))
    factors = 1
    for i in digits:
        if i == prevI:
            nI += 1
        else:
            factors *= fact(nI)
            prevI = i
            nI = 1

    factors *= fact(nI)

    return quantities // factors


def squareVal(num):
    n = num
    total = 0
    while n > 0:
        n10 = n % 10
        total += n10**2
        n = n // 10

    return total


def is89(num):
    n = num
    while True:
        if n == 89:
            return True
        elif n == 1:
            return False
        else:
            n = squareVal(n)


def challenge092():
    """ challenge092 """
    nDigits = 7

    n89 = 0
    for number in numbers([], 0, 10, nDigits):
        if is89(sum([i * i for i in number])):
            n89 += permutations(number)

    return n89
