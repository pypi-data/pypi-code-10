""" Challenge030 """


def challenge030():
    """ challenge030 """
    # Get maximum digits
    digits = 1
    per_digit = 9**5
    while (digits * per_digit) > (10**(digits)):
        digits += 1
    grand_total = 0
    for i in xrange(1, (9**5) * digits + 1):
        i = str(i)
        total = 0
        for digit in i:
            digit = int(digit)
            total += digit**5
        if total == int(i):
            grand_total += total
    return grand_total
