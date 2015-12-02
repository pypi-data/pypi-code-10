""" Challenge032 """
from pemjh.utilities.strings import permutate


def challenge032():
    """ challenge032 """
    source = "123456789"
    products = []
    for potential in [int(p) for p in permutate(source)]:
        # * can be after 1, 2, 3, 4
        # = can only be between 5 and 6
        third = potential % 10**4
        for i in xrange(1, 3):
            first = potential // 10**(9 - i)
            second = (potential // 10**(4)) % 10**(5 - i)
            product = first * second
            if product == third:
                products.append(third)

    return sum(set(products))
