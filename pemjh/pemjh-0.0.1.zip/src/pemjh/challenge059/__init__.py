""" Challenge059 """
from __future__ import with_statement
from itertools import cycle
from os.path import abspath, dirname


def decrypt(key, code):
    """
    >> from itertools import cycle
    >>> decrypt(cycle([42]), [107])
    [65]
    """
    decryption = []
    for number in code:
        ascii = number ^ key.next()
        # 65 - 90 = upper case
        # 97 - 123 = lower case
        # 48 - 57 = numbers
        # 32 - 64 = punctuation
        if (ascii >= 65 and ascii <= 90) or \
                (ascii >= 97 and ascii <= 123) or \
                (ascii >= 48 and ascii <= 57) or \
                (ascii >= 32 and ascii <= 64):
            decryption.append(ascii)
        else:
            return []

    return decryption


def challenge059():
    """ challenge059 """
    # Open file
    with open("%s/cipher1.txt" % dirname(abspath(__file__))) as cipher_file:
        numbers = list()
        for line in cipher_file:
            numbers.extend(line.split(","))
    numbers = [int(n) for n in numbers]

    # Load ints into an array
    # Lower case 97 - 122
    # Upper case 65 - 90
    for i in xrange(97, 123):
        for j in xrange(97, 123):
            for k in xrange(97, 123):
                key = cycle([i, j, k])

                decryption = decrypt(key, numbers)
                if decryption:
                    return sum(decryption)

    return False
