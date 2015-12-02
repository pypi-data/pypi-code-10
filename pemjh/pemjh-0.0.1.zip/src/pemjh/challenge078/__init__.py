""" Challenge078 """


def challenge078():
    """ challenge078 """
    n = 100000
    p = [1]*(n + 1)

    for i in xrange(1, n + 1):
        j, k, s = 1, 1, 0
        while j > 0:
            j = i - (3 * k * k - k) // 2
            if j >= 0:
                s -= (-1) ** k * p[j]
            j = i - (3 * k * k + k) // 2
            if j >= 0:
                s -= (-1) ** k * p[j]
            k += 1
        p[i] = s

        m = s % 1000000
        if m == 0:
            return i
