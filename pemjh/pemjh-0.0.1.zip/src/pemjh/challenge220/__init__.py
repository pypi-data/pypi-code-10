""" Challenge220 """


def dragonpos(n):
    c = [0, 1]
    length = 1
    while length < n:
        c = [c[0]+c[1], c[1]-c[0]]
        length *= 2

    if length == n:
        return c

    m = length - n
    c2 = dragonpos(m)
    c2 = [-c2[1], c2[0]]
    return [c[0]+c2[0], c[1]+c2[1]]


def challenge220():
    """ challenge220 """
    return ",".join(str(pos) for pos in dragonpos(10**12))
