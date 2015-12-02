""" Challenge055 """


def becomes_palindrome(potential):
    """
    >>> becomes_palindrome(47)
    True
    >>> becomes_palindrome(349)
    True
    >>> becomes_palindrome(196)
    False
    """
    working_n = str(potential)
    reverse = working_n[::-1]
    count = 0
    while True:
        working_n = str(int(working_n) + int(reverse))
        reverse = working_n[::-1]
        count += 1
        if working_n == reverse:
            return True
        if count > 50:
            return False


def challenge055():
    """ challenge055 """
    limit = 10000
    count = 0
    for potential in xrange(1, limit + 1):
        # Try to mirror
        if not becomes_palindrome(potential):
            count += 1
    return count
