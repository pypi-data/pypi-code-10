""" Challenge197 """


def f(x):
    return int(2**(30.403243784 - x**2)) * 10**(-9)


def challenge197():
    """ challenge197 """
    n = 10**12
    u = -1
    i = 0

    even = 0

    while i < n:
        u = f(u)
        i += 1

        if not i & 1:
            # Even
            if u == even:
                break
            even = u

    return u + f(u)
