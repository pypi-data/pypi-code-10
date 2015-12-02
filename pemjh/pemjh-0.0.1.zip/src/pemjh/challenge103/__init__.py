""" Challenge103 """


def subSets(l):
    # Split l into two seperate sets
    for i in xrange(2**(len(l))):
        setA = list()
        setB = list()
        # Deal 0 bits into setA
        for bit in xrange(len(l)):
            if ((2**bit & i) >> bit) == 0:
                setA.append(l[bit])
            else:
                setB.append(l[bit])
        yield setA, setB


def valid(l):
    # Loop through SetB
    for B, CPart in subSets(l):
        if len(B) > 0 and len(CPart) > 0:
            # Get subset C of CPart
            for C, _ in subSets(CPart):
                if len(C) > 0:
                    # Make sure B is always longer than C
                    if len(C) > len(B):
                        wB, wC = C, B
                    else:
                        wB, wC = B, C
                    # Check for correctness
                    if (len(wB) > len(wC)) and (sum(wB) <= sum(wC)):
                        # B should be more than C
                        return False
                    elif sum(wB) == sum(wC):
                        # Subsets should not be equal
                        return False

    return True


def challenge103():
    """ challenge103 """
    prev = [11, 18, 19, 20, 22, 25]

    # Get center numbers
    midPoint = float(len(prev)) / 2

    if midPoint == int(midPoint):
        centers = [prev[int(midPoint)], prev[int(midPoint) + 1]]
    else:
        centers = [prev[int(midPoint) + 1]]

    ans = None
    sumAns = None
    for b in centers:
        newSet = [b] + [b + a for a in prev]
        if sum(newSet) < sumAns or sumAns is None:
            if valid(newSet):
                ans = newSet
                sumAns = sum(newSet)

    return int("".join([str(i) for i in ans]))
