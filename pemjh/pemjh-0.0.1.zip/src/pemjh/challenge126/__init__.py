""" Challenge126 """


def surroundingCubes(x, y, z, layer):
    return (x * y + x * z + y * z) * 2 + (x + y + z + layer - 2) * 4 * \
        (layer - 1)


def challenge126():
    """ challenge126 """
    maximumResult = 19000

    results = [0] * maximumResult

    maximumDepth = 1
    while(surroundingCubes(1, 1, 1, maximumDepth) < maximumResult):
        maximumDepth += 1

    for depth in xrange(1, maximumDepth):
        maximumA = 1
        while(surroundingCubes(maximumA, 1, 1, depth) < maximumResult):
            maximumA += 1
        for a in xrange(1, maximumA):
            maximumB = 1
            while(surroundingCubes(a, maximumB, 1, depth) < maximumResult
                  and maximumB <= a):
                maximumB += 1
            for b in xrange(1, maximumB):
                maximumC = 1
                while(surroundingCubes(a, b, maximumC, depth) < maximumResult
                      and maximumC <= b):
                    maximumC += 1
                for c in xrange(1, maximumC):
                    cubes = surroundingCubes(a, b, c, depth)

                    if(cubes >= maximumResult):
                        break
                    else:
                        results[cubes] += 1

    for i in xrange(maximumResult):
        if results[i] == 1000:
            return i
