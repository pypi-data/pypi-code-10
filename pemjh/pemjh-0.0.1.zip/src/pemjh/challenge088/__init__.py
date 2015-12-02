""" Challenge088 """


def findPossibleProducts(limit, known=dict()):

    if limit in known:
        return known[limit]

    products = set()

    multi = 2
    while multi <= limit:
        for multi2, s, d in findPossibleProducts(limit // multi):
            products.add((multi * multi2, s + multi, d + 1))

        products.add((multi, multi, 1))
        multi += 1

    known[limit] = products
    return products


def challenge088():
    """ challenge088 """
    limit = 12000
    found = [2 * i for i in xrange(limit + 1)]

    for pr, s, d in set(findPossibleProducts(limit * 2)):
        # Get digits so that s == pr
        digits = pr - s + d
        if digits <= limit and found[digits] > pr:
            found[digits] = pr

    return sum(set(found[2:]))
