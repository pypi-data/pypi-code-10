""" Challenge112 """


def isBouncy(n):
    d, m = divmod(n, 10)
    movement = 0
    while d > 0:
        # get the new movement
        d, nextM = divmod(d, 10)
        if nextM < m:
            nextMovement = -1
        elif nextM > m:
            nextMovement = 1
        else:
            nextMovement = 0

        m = nextM

        if nextMovement != 0:
            # A move found

            # Compare to previous movements
            if movement == 0:
                # First directional movement
                movement = nextMovement
            elif movement != nextMovement:
                # Change in direction found
                return True
    return False


def challenge112():
    """ challenge112 """
    target = 99
    currentBouncy = 0
    currentNumber = 100
    bouncy = list()
    while True:
        if isBouncy(currentNumber):
            currentBouncy += 100
            bouncy.append(currentNumber)

        if (currentBouncy / currentNumber) >= target:
            break

        currentNumber += 1

    return currentNumber
