""" Challenge095 """


def divisors(n):
    nums = [0] * (n + 1)
    nums[1] = 1
    for root in xrange(1, n + 1):
        for inc in xrange(2 * root, n + 1, root):
            nums[inc] += root

    return nums


def chainLengths(n):
    # Create memory
    known = divisors(n)

    chains = [0] * (n + 1)
    for x in xrange(1, n + 1):

        if chains[x]:
            continue

        visited = [x]

        # Within limit
        # Unknown chain
        # Not visited yet
        while (known[visited[-1]] <= n) and \
                (chains[known[visited[-1]]] == 0) and \
                known[visited[-1]] not in visited:
            visited.append(known[visited[-1]])

        # Found a new loop?
        if known[visited[-1]] in visited:
            loop = visited.index(known[visited[-1]])
            for i in range(loop):
                chains[visited[i]] = -1

            lChain = len(visited) - loop

            for i in range(loop, len(visited)):
                chains[visited[i]] = lChain

        else:
            # Bad sequence
            for i in visited:
                chains[i] = -1

    return chains


def challenge095():
    """ challenge095 """
    limit = 1000000

    chains = chainLengths(limit)
    highest = max(chains)
    lowest = chains.index(highest)
    return lowest
