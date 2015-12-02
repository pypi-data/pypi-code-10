""" Challenge105 """
from __future__ import with_statement
from os.path import abspath, dirname


def sizedSubsets(l, size):
    subsets = list()
    sizeL = len(l)
    for index in range(len(l)):

        if size > (sizeL - index):
            break

        # More needed?
        if size > 1:
            for sub in sizedSubsets(l[index + 1:], size - 1):
                subsets.append([l[index]] + sub)
        else:
            subsets.append([l[index]])

    return subsets


def checkForDuplicateSetSums(l):
    for setSize in range(1, len(l) // 2 + 1):
        sumSub = [sum(seq) for seq in sizedSubsets(l, setSize)]
        sumSub.sort()
        if len(sumSub) != len(set(sumSub)):
            # Remove duplicates should be identical
            return False
    return True


def valid(l):
    # Sort it
    l.sort()
    # Check that all greater sized sets are bigger than smaller sized ones
    # Get the largest set from small numbers and the smaller set from large
    # numbers
    nItems = len(l)

    if nItems & 1:
        large = l[:(nItems // 2) + 1]
    else:
        large = l[:(nItems // 2)]

    small = l[(nItems // 2) + 1:]

    if sum(large) <= sum(small):
        return False

    return checkForDuplicateSetSums(l)


def challenge105():
    """ challenge105 """
    # Open the file
    with open("%s/sets.txt" % dirname(abspath(__file__))) as f:
        ans = 0

        for seq in [[int(i) for i in line.strip().split(',')] for line in f]:
            if valid(seq):
                ans += sum(seq)

        return ans
