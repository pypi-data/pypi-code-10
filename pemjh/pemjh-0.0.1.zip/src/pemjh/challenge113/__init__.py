""" Challenge113 """
from pemjh.utilities.numbers import polytopicNumbers


def challenge113():
    """ challenge113 """
    digits = 100
    ascending = sum(polytopicNumbers(digits - 1, 10))
    # Remove the non-rising
    # 0*-9*
    ascending -= 10

    # Remove more from ascending
    # 0..xxxx
#    ascending -= 9 * (digits - 1)

    # Set descending to the same for now
    descending = sum(polytopicNumbers(digits - 1, 10)) - 1

    # Add leading zero numbers
    for d in xrange(1, digits):
        p = sum(polytopicNumbers(d - 1, 10)) - 10
        descending += p

    # 2 Digits
    # Rising
    # 12, 13, 14, 15, 16, 17, 18, 19 - 8
    # 23, 24, 25, 26, 27, 28, 29 - 7
    # 34, 35, 36, 37, 38, 39 - 6
    # 45, 46, 47, 48, 49 - 5
    # 56, 57, 58, 59 - 4
    # 67, 68, 69 - 3
    # 78, 79 - 2
    # 89 - 1
    # 36

    # Falling
    # 10 - 1
    # 20, 21 - 2
    # 30, 31, 32 - 3
    # 40, 41, 42, 43 - 4
    # 50, 51, 52, 53, 54 - 5
    # 60, 61, 62, 63, 64, 65 - 6
    # 70, 71, 72, 73, 74, 75, 76 - 7
    # 80, 81, 82, 83, 84, 85, 86, 87 - 8
    # 90, 91, 92, 93, 94, 95, 96, 97, 98 - 9
    # 45

    # Flat
    # 1, 2, 3, 4, 5, 6, 7, 8, 9 - 9
    # 11, 22, 33, 44, 55, 66, 77, 88, 99 - 9
    # 18

    # 99

    return ascending + descending
