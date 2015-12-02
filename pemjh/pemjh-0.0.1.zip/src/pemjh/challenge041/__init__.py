""" Challenge041 """
from pemjh.utilities.numbers import isPrime
from pemjh.utilities.strings import permutate


def challenge041():
    """ challenge041 """
    # loop through number of digits
    highest = 0
    for number_size in [4, 7]:
        chars = "".join([str(c) for c in xrange(1, number_size + 1)])
        for potential in [int(p) for p in permutate(chars) if isPrime(int(p))]:
            if potential > highest:
                highest = potential

    return highest
