""" Challenge090 """
from copy import copy
from itertools import chain


def get6Combs(cube):
    c6 = cube.count('6')
    if c6 == 0:
        yield cube
    elif c6 == 1:
        # Flip it either way
        i6 = cube.index('6')
        yield cube[:i6] + '6' + cube[i6 + 1:]
        yield cube[:i6] + '9' + cube[i6 + 1:]
    else:  # 2
        # 69 and 96
        i6 = cube.index('6')
        i62 = cube[i6 + 1:].index('6') + i6 + 1
        yield cube[:i6] + '6' + cube[i6 + 1: i62] + '9' + cube[i62 + 1:]
        yield cube[:i6] + '9' + cube[i6 + 1: i62] + '6' + cube[i62 + 1:]


def fillRemaining(cube):
    for i in range(9):
        if validAddition(cube, str(i)):
            if len(cube) == 5:
                yield cube + str(i)
            else:
                for sub in fillRemaining(cube + str(i)):
                    yield sub


def validAddition(cube, newFace):
    if newFace == '6':
        return cube.count('6') < 2
    else:
        return cube.count(newFace) == 0


def amendCubesForSquare(cube0, cube1, square):
    successful = []
    # Options for suitable cubes are:

    # Using existing on both
    # Check that both exist
    if square[0] in cube0 and square[1] in cube1:
        # No amending required
        successful.append((copy(cube0), copy(cube1)))

    # Using existing on 0 but new on 1
    if square[0] in cube0:
        newCube1 = cube1 + square[1]
        # if square[1] is 6 then make sure only one other exists
        # else make sure no other exists
        # Check no more than 6 sides
        if validAddition(cube1, square[1]) and len(newCube1) <= 6:
            successful.append((copy(cube0), newCube1))

    # Using existing on 1 but new on 0
    if square[1] in cube1:
        newCube0 = cube0 + square[0]
        # Check no more than 6 sides
        if validAddition(cube0, square[0]) and len(newCube0) <= 6:
            successful.append((newCube0, copy(cube1)))

    # Using new on both
    newCube0 = cube0 + square[0]
    newCube1 = cube1 + square[1]
    if validAddition(cube0, square[0]) and \
            validAddition(cube1, square[1]) and \
            len(newCube0) <= 6 and len(newCube1) <= 6:
        successful.append((newCube0, newCube1))

    return successful


def buildCubes(cube0, cube1, squaresLeft):
    # Get next square
    nextSquare = squaresLeft[0]

    # Try building the square using cube0 for digit 0
    suitableCubes = amendCubesForSquare(cube0, cube1, nextSquare)

    # Try building the square using cube1 for digit 0
    suitableCubes.extend(amendCubesForSquare(cube1, cube0, nextSquare))

    if len(squaresLeft) > 1:
        # Pass each down to build more cubes
        for cubes in suitableCubes:
            for complete in buildCubes(cubes[0], cubes[1], squaresLeft[1:]):
                yield complete
    else:
        # sort each cubes so that cube 0 is the lowest
        # yield each pair of cubes
        for cubes in suitableCubes:
            if len(cubes[0]) == 6:
                cube0s = [cubes[0]]
            else:
                cube0s = fillRemaining(cubes[0])

            if len(cubes[1]) == 6:
                cube1s = [cubes[1]]
            else:
                cube1s = fillRemaining(cubes[1])

            # Get 6 combs for each
            cube0s = list(chain(*[list(get6Combs(c)) for c in cube0s]))
            cube1s = list(chain(*[get6Combs(c) for c in cube1s]))

            # Sort the cubes
            cube0s = ["".join(sorted(c)) for c in cube0s]
            cube1s = ["".join(sorted(c)) for c in cube1s]

            for c0 in cube0s:
                for c1 in cube1s:
                    if c0 < c1:
                        yield (c0, c1)
                    else:
                        yield (c1, c0)


def challenge090():
    """ challenge090 """
    squareNumbers = ['01', '04', '06', '16', '25', '36', '46', '64', '81']

    # Build cubes
    cube0 = ''
    cube1 = ''
    return len(sorted(set(buildCubes(cube0, cube1, squareNumbers))))
