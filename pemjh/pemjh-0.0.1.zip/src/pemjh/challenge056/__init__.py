""" Challenge056 """


def challenge056():
    """ challenge056 """
    highest = 0
    for base in xrange(1, 100):
        for index in xrange(1, 100):
            val = base**index
            val = str(val)
            total = sum([int(c) for c in val])
            if total > highest:
                highest = total

    return highest
