""" Challenge134 """
from pemjh.utilities.numbers import sievedPrimes


def jumpSize(t, c, s):
    if t == c:
        return 0

    # s will always be 1, 3, 7, or 9
    if s == 1:
        cycle = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    elif s == 3:
        cycle = [3, 6, 9, 2, 5, 8, 1, 4, 7, 0]
    elif s == 7:
        cycle = [7, 4, 1, 8, 5, 2, 9, 6, 3, 0]
    else:
        cycle = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

    # Find c in cycle
    cInd = cycle.index(c)

    # Find t in cycle
    tInd = cycle.index(t)

    # Is t after c?
    if t in cycle[cInd:]:
        return tInd - cInd
    else:
        return 10 - cInd + tInd


def f(target, current, step):
    # Get the last digit of step
    s = step % 10
    # Get the last digit of current
    c = current % 10
    # Get the last digit of target
    t = target % 10

    # Get the amount to jump step by to get to the target digit
    jump = jumpSize(t, c, s) * step
    current += jump

    # If target >= 10, recur
    if target >= 10:
        return f(target // 10, current // 10, step) * 10 + t
    else:
        return current


def challenge134():
    """ challenge134 """
    limit = 10**6
    primes = sievedPrimes(limit + (limit / 10))
    # Strip pre 5
    for _ in xrange(3):
        primes.next()

    p1 = primes.next()
    S = 0
    for p2 in primes:
        if p1 > limit:
            break

        # f(target, current, step)
        n = f(p1, p2, p2)

        S += n

        p1 = p2
    return S
