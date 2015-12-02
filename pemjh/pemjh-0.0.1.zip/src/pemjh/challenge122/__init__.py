""" Challenge122 """


def challenge122():
    """ challenge122 """
    limit = 200

    best = [None, [set([1])]]

    for i in xrange(2, limit + 1):
        # Loop through from 1 to half i
        facts = list()
        for j in xrange(1, i // 2 + 1):

            # Get list of sums
            for f in best[i - j]:

                # Is j in sumB?
                if j in f:
                    # Add sumB + i to the sums
                    facts.append(f.union([i]))

        # Get the shortest
        shortest = min(len(eq) for eq in facts)
        best.append([eq for eq in facts if len(eq) == shortest])

    return sum([len(s[0]) - 1 for s in best[1:]])
