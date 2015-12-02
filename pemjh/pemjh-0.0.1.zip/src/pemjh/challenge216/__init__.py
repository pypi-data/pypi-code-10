""" Challenge216 """
import math


def l(a, b):
    k = 1
    while a:
        v = 0
        while a % 2 == 0:
            v += 1
            a /= 2
        if v % 2 and b % 8 in (3, 5):
            k = -k
        if b > a:
            if a % 4 == 3 and b % 4 == 3:
                k = -k
            b, a = a, b - a
        else:
            a -= b
    return 0 if b > 1 else k


def sq(a, p):
    q, e = p - 1, 0
    while q % 2 == 0:
        e += 1
        q //= 2
    n = 2
    while l(n, p) == 1:
        n += 1
    z = pow(n, q, p)
    y, r, x = z, e, pow(a, (q - 1) // 2, p)
    b = a * x ** 2 % p
    x = a * x % p
    while b % p != 1:
        bb, m = b, 0
        while bb != 1:
            bb = bb ** 2 % p
            m += 1
        if m == r:
            return 0
        t = y
        for _ in range(r - m - 1):
            t = t ** 2 % p
        y, r, x = t ** 2 % p, m, x * t % p
        b = b * y % p
    return x


def challenge216():
    """ challenge216 """
    nmax = 50000000

    primes = int(math.sqrt(2 * nmax ** 2)) * [True]

    primes[0:2] = [False, False]

    for x in range(2, int(math.sqrt(len(primes)) + 1)):
        if primes[x]:
            for y in range(2 * x, len(primes), x):
                primes[y] = False

    t = (nmax + 1) * [True]

    t[0:2] = [False, False]

    for x in range(3, len(primes)):
        if primes[x]:
            s = sq((x + 1) // 2, x)
            if s:
                for i in range(s, len(t), x):
                    if 2 * i ** 2 - 1 != x:
                        t[i] = False
                for i in range(x - s, len(t), x):
                    if 2 * i ** 2 - 1 != x:
                        t[i] = False

    return sum(1 for i in range(len(t)) if t[i])
