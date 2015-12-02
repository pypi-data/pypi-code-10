""" Challenge068 """


def get_pairs(score, choice):
    """ Generate pairs of numbers from choice that add up to score """
    for i in [i for i in choice if i < score]:
        j = score - i
        if j in [x for x in choice if x is not i]:
            yield i, j


def get_spokes(score, start, start_index, choice, num_spokes):
    """ Generate groups of pairs """
    for i, j in get_pairs(score - start, choice):
        spoke = [i, j]
        spoke.insert(start_index, start)

        if num_spokes == 1:
            yield [spoke]

        else:
            # Find further spokes
            left = [x for x in choice if x != i and x != j]
            for next_spokes in get_spokes(score,
                                          spoke[2],
                                          1,
                                          left,
                                          num_spokes - 1):
                spokes = [spoke]
                spokes.extend(next_spokes)
                yield spokes


def challenge068():
    """ challenge068 """
    results = []
    limit = 5

    # 5 spokes, 10 on the outside of one
    # spokes could be 13 (10,1,2) to 27(10,9,8)
    for score in xrange(3, 18):

        # Finish the 10 spoke
        choice = set(range(1, 10))

        for solution in get_spokes(score, 10, 0, choice, limit - 1):
            # Get all of the numbers
            used = [solution[0][1], solution[0][2]]
            for i in xrange(limit - 1):
                used.append(solution[i][0])
                used.append(solution[i][2])

            left = list(choice.difference(set(used)))

            if left[0] + solution[limit - 2][2] + solution[0][1] == score:
                solution.extend([[left[0],
                                  solution[limit - 2][2],
                                  solution[0][1]]])

                start = 0
                highest = 10
                for index, spoke in enumerate(solution):
                    if spoke[0] != 10:
                        if spoke[0] < highest:
                            start = index
                            highest = spoke[0]

                for _ in xrange(start):
                    solution.append(solution[0])
                    solution.pop(0)

                result = []
                for spoke in solution:
                    for i in spoke:
                        result.append(str(i))

                results.append(int("".join(result)))

    return max(results)
