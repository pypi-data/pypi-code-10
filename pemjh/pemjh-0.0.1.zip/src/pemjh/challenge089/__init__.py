""" Challenge089 """
# I = 1
# V = 5
# X = 10
# L = 50
# C = 100
# D = 500
# M = 1000

#    1. Only I, X, and C can be used as the leading numeral in part of
#       a subtractive pair.
#    2. I can only be placed before V and X.
#    3. X can only be placed before L and C.
#    4. C can only be placed before D and M.

from __future__ import with_statement
from os.path import abspath, dirname

convertChar = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000}


def decypherNumeral(s):

    total = 0
    prev = 0
    currentTotal = 0
    for v in [convertChar[c] for c in s]:
        # Is v greater than previous?
        if v > prev:
            currentTotal = v - prev
        elif v == prev:
            currentTotal += v
        else:
            total += currentTotal
            currentTotal = v
        prev = v

    total += currentTotal

    return total


def getNumeral(n):
    divisors = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
                [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
                [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'],
                [1, 'I']]

    numeral = []
    working = n
    for div, c in divisors:
        nDiv, working = divmod(working, div)
        numeral.extend([c] * nDiv)

    return "".join(numeral)


def getRomanNumeralSaving(s):
    # Get length of numeral
    preLength = len(s)

    # Get value of numeral
    value = decypherNumeral(s)

    # Get optimised length of numeral
    newNumeral = getNumeral(value)
    newLength = len(newNumeral)

    # Return difference
    return preLength - newLength


def challenge089():
    """ challenge089 """
    # Open the numeral file
    with open("%s/roman.txt" % dirname(abspath(__file__))) as f:
        # Get saving of roman numeral
        return sum(getRomanNumeralSaving(s.strip()) for s in f)
