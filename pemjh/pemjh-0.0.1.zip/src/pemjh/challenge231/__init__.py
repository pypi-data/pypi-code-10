""" Challenge231 """
from pemjh.utilities.numbers import sievedPrimes


def getFirstMultipleOnOrAfter(target, divisor):
    m = target % divisor
    if m:
        return target + (divisor - m)
    else:
        return target


def getFirstMultipleOnOrBefore(target, divisor):
    m = target % divisor
    if m:
        return target - m
    else:
        return target


def numInRange(start, end, step):
    start = start // step
    end = end // step

    return end - start + 1


def challenge231():
    """ challenge231 """
    n = 20000000
    k = 15000000
    # Get the primes needed
    primes = sievedPrimes(n)
    # Remove 1
    primes.next()

    total = 0
    # Cycle through primes
    for p in primes:
        current = 1
        # Loop through indexes of p
        while 1:
            current *= p

            # Get numerator range
            # Get first multiple on or after n - k
            # Get first multiple before n
            numRange = (getFirstMultipleOnOrAfter(n - k + 1, current),
                        getFirstMultipleOnOrBefore(n, current))

            # Get denominator range
            # Get first multiple on or after 1
            # Get first multiple before k
            denRange = (getFirstMultipleOnOrAfter(1, current),
                        getFirstMultipleOnOrBefore(k, current))

            # Record if either is in range
            inRange = False
            # Check each is in range,
            # If in range then get the number of multiples in range
            # Multiply by p and add to sum
            if numRange[0] <= numRange[1]:
                total += numInRange(numRange[0], numRange[1], current) * p
                inRange = True
            if denRange[0] <= denRange[1]:
                total -= numInRange(denRange[0], denRange[1], current) * p
                inRange = True

            if not inRange:
                break

    return total
