""" Challenge074 """
from pemjh.utilities.numbers import fact


def fact_sum(facts, num):
    """ Return collection of factorials for each digit in num """
    return sum([facts[c] for c in str(num)])


def chain_size(num, known):
    """ Get the size of the chain starting with num """
    route = set([num])
    facts = dict((str(i), fact(i)) for i in xrange(0, 10))
    step = fact_sum(facts, num)
    first_step = step
    route_length = 1
    while step not in route:
        if step in known:
            size = route_length + known[step]
            known[first_step] = size - 1
            known[num] = size
            return size
        else:
            route_length += 1
            route.add(step)
            step = fact_sum(facts, step)

    known[first_step] = route_length - 1
    known[num] = route_length
    return route_length


def challenge074():
    """ challenge074 """
    limit = 1000000
    count = 0
    known = {}
    for i in xrange(1, limit + 1):
        size = chain_size(i, known)
        if size == 60:
            count += 1
    return count
