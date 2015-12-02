""" Challenge003 """


def challenge003():
    """ challenge003 """
    # Loop from 2 until the target number is 1
    target = 600851475143

    current = 2
    # Loop until target is 1
    while True:
        # Loop until the mod of target divided by current is not 0

        while True:
            remainder = target % current
            if not remainder:
                target /= current
            else:
                break

        if target == 1:
            break

        current += 1

    return current
