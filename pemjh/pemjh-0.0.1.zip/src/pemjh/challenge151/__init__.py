""" Challenge151 """


def batch(a5, a4, a3, a2):
    ans = 0.0
    total = float(a5 + a4 + a3 + a2)

    if total == 1 and a5 != 1:
        ans = 1.0

    if a5 > 0:
        ans += a5 * batch(a5 - 1, a4, a3, a2)
    if a4 > 0:
        ans += a4 * batch(a5 + 1, a4 - 1, a3, a2)
    if a3 > 0:
        ans += a3 * batch(a5 + 1, a4 + 1, a3 - 1, a2)
    if a2 > 0:
        ans += a2 * batch(a5 + 1, a4 + 1, a3 + 1, a2 - 1)

    if total > 0:
        ans /= total

    return ans


def challenge151():
    """ challenge151 """
    return round(batch(1, 1, 1, 1), 6)
