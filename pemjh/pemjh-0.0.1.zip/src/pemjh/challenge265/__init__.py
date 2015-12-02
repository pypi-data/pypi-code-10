""" Challenge265 """


def tobin(h):
    d, m = divmod(h, 8)
    s = "1" if d > 0 else "0"
    d, m = divmod(m, 4)
    s += "1" if d > 0 else "0"
    d, m = divmod(m, 2)
    s += "1" if d > 0 else "0"
    s += "1" if m > 0 else "0"
    return s


def binary(n, d):
    # convert to hex string
    b = "".join([tobin(int(c, 16)) for c in hex(n)[2:]])[-d:]

    return "0" * (d - len(b)) + b


def digits(n):
    return [binary(v, n) for v in xrange(2**n)]


def getSequences(prefix, remaining):
    if len(remaining) == 0:
        return [""]  # Don't return the final 0

    seq = list()
    # Find those with the prefix at the start + ?
    for b in xrange(2):
        if (prefix + str(b)) in remaining:
            # Create new remaining
            remain = [s for s in remaining if s != (prefix + str(b))]
            for s in getSequences((prefix + str(b))[1:], remain):
                seq.append(prefix[0] + s)

    return seq


def S(n):
    # Get all options for n
    options = digits(n)

    # Get sequences
    options.remove("0" * n)
    seq = getSequences("0" * (n - 1), options)

    # Convert to numbers
    seq = [int(s, 2) for s in seq]

    # Return sum
    return sum(seq)


def challenge265():
    """ challenge265 """
    return S(5)
