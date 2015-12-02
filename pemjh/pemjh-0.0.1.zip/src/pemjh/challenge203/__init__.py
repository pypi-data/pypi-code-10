""" Challenge203 """
from pemjh.utilities.numbers import sievedPrimes


def challenge203():
    """ challenge203 """
    rows = 51

    nums = set()

    # Generate triangle
    row = [1] * rows
    while len(row) > 0:
        # Remove last
        row = row[:-1]

        for i in xrange(1, len(row)):
            row[i] += row[i - 1]

        nums.update(row)

    # Get maximum
    highest = max(nums)

    # Get primes up to root of highest
    primes = list([x**2 for x in sievedPrimes(int(highest**0.5) + 1)])[1:]

    squareFree = []

    for n in nums:
        free = True
        for p in primes:
            if p > n:
                break
            if n % p == 0:
                free = False
                break

        if free:
            squareFree.append(n)

    return sum(squareFree)
