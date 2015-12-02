""" Challenge036 """


def get_binary_string(number):
    """ Get the binary representation of the input (most significant to the
    right
    >>> get_binary_string(7)
    '111'
    >>> get_binary_string(2)
    '01'
    >>> get_binary_string(26)
    '01011'
    >>> get_binary_string(0)
    ''
    """
    remaining = number
    binary_string = ""
    while remaining > 0:
        binary_string += str(remaining % 2)
        remaining = remaining >> 1
    return binary_string


def challenge036():
    """ challenge036 """
    decimals = []

    # Ignore 2s, since they would end in 0 and not be suitable
    for i in xrange(1, 1000000, 2):
        decimal_string = str(i)
        # Is the decimal palindromic?
        if decimal_string == decimal_string[::-1]:
            binary_string = get_binary_string(i)
            if binary_string == binary_string[::-1]:
                decimals.append(i)
    return sum(decimals)
