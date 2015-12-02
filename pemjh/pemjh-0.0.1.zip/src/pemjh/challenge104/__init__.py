""" Challenge104 """


def myEnumerate(seq, start=0):
    i = start
    for item in seq:
        yield [i, item]
        i += 1


def fiboTrunc(trunc):
    aStart, bStart = 0, 1
    aEnd, bEnd = 0, 1

    endTrunc = 10**trunc
    startTrunc = 10**(trunc + 8)

    while 1:
        # Add,
        aStart, bStart = bStart, aStart + bStart
        aEnd, bEnd = bEnd, aEnd + bEnd

        # Skim
        aEnd = aEnd % endTrunc
        bEnd = bEnd % endTrunc

        while aStart >= startTrunc:
            aStart /= 10
            bStart /= 10

        aStartRet = aStart
        while aStartRet > endTrunc:
            aStartRet /= 10

        # Return
        yield aStartRet, aEnd


def challenge104():
    """ challenge104 """
    lowerLimit = 123456788  # Must be at least greater than this
    for k, f in myEnumerate(([s, e] for s, e in fiboTrunc(9)), start=1):
        s = f[0]
        e = f[1]
        if s > lowerLimit and e > lowerLimit and \
                "".join(sorted(str(s))) == "123456789" and \
                "".join(sorted(str(e))) == "123456789":
            return k
    return

answer = 329468

if __name__ == "__main__":
    print challenge104()
