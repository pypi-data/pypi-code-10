""" Challenge131 """
from pemjh.utilities.numbers import sievedPrimes


def challenge131():
    """ challenge131 """
    limit = 1000000
    primes = list(sievedPrimes(limit))

    # n**3 + n**2*p = m**3
    # n**2 * (n + p) = m**3
    # (n + p) = m**3 / n**2
    # p = (m**3 - n**3) / n**2
    # n is a cube, a**3
    # Cubes where the difference between them is a multiple of n**2

    found = 0

    for p in primes:
        # Find two cubes that have a difference of p
        lowerCube = 1
        upperCube = 2

        while 1:
            diff = upperCube**3 - lowerCube**3
#            print diff
            if diff > p:
                lowerCube += 1
                if lowerCube == upperCube:
                    # Couldn't find
                    break
            elif diff < p:
                upperCube += 1
            else:
                # Found
                found += 1
                break

    return found
