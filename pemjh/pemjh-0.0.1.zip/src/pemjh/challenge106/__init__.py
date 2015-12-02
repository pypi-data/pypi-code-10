""" Challenge106 """


def incrementTrilist(trl):
    rightIndex = len(trl) - 1
    # If the rightmost is 2 then increment the left part
    if trl[rightIndex] == 2:
        if rightIndex == 0:
            # No more incrementing possible.. shouldn't happen???
            pass
        else:
            pre = trl[:rightIndex]
            incrementTrilist(pre)
            trl[:rightIndex] = pre
            trl[rightIndex] = 0
    else:
        trl[rightIndex] += 1


def allSubsets(size):
    triList = [0] * size

    for i in xrange(3**size - 1):
        incrementTrilist(triList)
        # Must be a 1 and a 2 in the list
        if triList.count(1) > 0 and triList.count(2) > 0:
            # 2 cannot be before the first 1
            if triList.index(2) > triList.index(1):
                # Count of 1 and 2 should be equal
                yield [i for i in triList]


def score(l):
    working = [v for v in l]

    # Assume first value of l is a 1, a value of 2 otherwise is a pass
    while len(working) > 0:
        # If the next value is a 2 then return pass
        if working[0] == 2:
            return True

        # Remove the leading 1
        working = working[1:]

        # Find the next 2 (there should be one since 1,2 in pairs)
        index2 = working.index(2)

        # Remove the 2
        working.pop(index2)

    return False


def getRequiredCompares(size):
    allS = list(allSubsets(size))

    # Filter to only those with equal numbers of 1 and 2, rule ii
    workingS = [s for s in allS if s.count(1) == s.count(2)]

    # Filter out those with size 1 subsets, we already know these cannot be
    # equal
    workingS = [s for s in workingS if s.count(1) != 1]

    # Score all the sequences and return those that balance
    workingS = [s for s in workingS if score([a for a in s if a != 0])]

    return len(workingS)


def challenge106():
    """ challenge106 """
    return getRequiredCompares(12)
