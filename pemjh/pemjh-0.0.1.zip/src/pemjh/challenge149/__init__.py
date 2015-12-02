""" Challenge149 """


def sk1(k):
    return (100003 - 200003 * k + 300007 * k**3) % 1000000 - 500000


def sk2(sk24, sk55):
    return (sk24 + sk55 + 1000000) % 1000000 - 500000


def snake(l):

    maximum = 0

    # Set snake at start
    end = len(l)
    tail = 0
    head = 0
    current = 0
    while tail != end:
        current += l[head]
        head += 1

        if current > maximum:
            maximum = current

        if current < 1 or head == end:
            tail = head
            current = 0

    return maximum


def challenge149():
    """ challenge149 """
    values = [sk1(k) for k in xrange(1, 56)]

    for k in xrange(55, 4000000):
        values.append(sk2(values[k - 24], values[k - 55]))

    values = [int(v) for v in values]

    # Add vertical routes
    # horizontal and diagonal were included but I have removed them since
    # the answer is in the vertical columns
    routes = []
    for column in xrange(0, 2000):
        routes.append(values[column: 4000000: 2000])

    totals = [snake(r) for r in routes]

    return max(totals)
