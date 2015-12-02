""" Challenge040 """


def challenge040():
    """ challenge040 """
    indexes = [1, 10, 100, 1000, 10000, 100000, 1000000]

    current_n = 0
    current_integer = 0
    total = 1
    for index in indexes:
        while current_n < index:
            current_integer += 1
            current_n += len(str(current_integer))
        total *= int(str(current_integer)[index - current_n - 1])

    return total
