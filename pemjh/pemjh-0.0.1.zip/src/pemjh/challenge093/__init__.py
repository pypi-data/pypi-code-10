""" Challenge093 """
import operator


def combinations(left):
    nLeft = len(left)
    for i in left:
        if nLeft > 1:
            for com in combinations([j for j in left if j != i]):
                yield [i] + com
        else:
            yield [i]


def selection(l, left):
    for v in l:
        if left > 1:
            for sel in selection(l, left - 1):
                yield [v] + sel
        else:
            yield [v]


def equatedNumbers(a, b, c, d, operators):
    nums = list()

    for ops in operators:
        # ((w ? x) ? y) ? z
        nums.append(ops[2](ops[1](ops[0](a, b), c), d))

        # (w ? (x ? y)) ? z
        nums.append(ops[2](ops[0](a, ops[1](b, c)), d))

        # (w ? x) ? (y ? z)
        nums.append(ops[1](ops[0](a, b), ops[2](c, d)))

        # w ? ((x ? y) ? z)
        try:
            nums.append(ops[0](a, ops[2](ops[1](b, c), d)))
        except:
            pass

        # w ? (x ? (y ? z))
        try:
            nums.append(ops[0](a, ops[1](b, ops[2](c, d))))
        except:
            pass

    return [int(n) for n in nums if n == int(n) and n > 0]


def challenge093():
    """ challenge093 """
    maximum = 60

    highest = (0, 0, 0, 0, 0)

    operators = list(selection([operator.add, operator.sub,
                                operator.mul, operator.truediv], 3))

    for a in xrange(1, 10):
        for b in xrange(a + 1, 10):
            for c in xrange(b + 1, 10):
                for d in xrange(c + 1, 10):

                    nums = [False] * maximum

                    # Get sequences of abcd
                    for com in combinations([a, b, c, d]):
                        for n in equatedNumbers(com[0],
                                                com[1],
                                                com[2],
                                                com[3],
                                                operators):
                            if n < maximum:
                                nums[n] = True

                    # Find first
                    lowest = nums[1:].index(False)

                    if lowest > highest[0]:
                        highest = (lowest, a, b, c, d)

                    if lowest == 0:
                        break

                if d == c + 1:
                    break
            if c == b + 1:
                break
        if b == a + 1:
            break

    return highest[1] * 1000 + highest[2] * 100 + highest[3] * 10 + highest[4]
