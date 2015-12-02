""" Challenge118 """
from pemjh.utilities.numbers import PrimeChecker
from itertools import permutations


def too_long(current_length, last_length):
    return (9 - current_length) > 0 and (9 - current_length < last_length)


def valid(num):
    return len(set(num)) == len(num)


def build_sets(existing, left, lExist=0):
    sets = 0
    for prime_index in xrange(len(left)):
        new = existing + left[prime_index]

        lLeft = len(left[prime_index])
        lNew = lExist + lLeft

        if lNew > 9:
            # Cannot be any more
            break
        elif lNew < 9 and (9 - lNew < lLeft):
            continue

        if valid(new):
            if lNew == 9:
                sets += 1
            else:
                sets += build_sets(new, left[prime_index + 1:], lNew)
    return sets


def challenge118():
    """ challenge118 """
    pc = PrimeChecker()
    perms = ["1", "2", "3", "5", "7"]
    for size in xrange(2, 10):
        perms.extend([l for l in permutations("123456789", size)
                      if l[-1] != 2 and l[-1] != "5"])

    perms = ["".join(p) for p in perms]

    primes = [prime for prime in perms if pc.isPrime(int(prime))]

    sets = build_sets("", primes)

    return sets
