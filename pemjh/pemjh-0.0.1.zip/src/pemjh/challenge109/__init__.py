""" Challenge109 """


def getNonDoubleOuts(n, darts, nums, known=dict()):
    key = (n, darts, tuple(nums))
    if key in known:
        return known[key]

    nCount = 0
    for d in nums:
        if d[0] > n:
            break
        left = n - d[0]

        if left == 0:
            nCount += 1
        elif darts > 1:
            nCount += getNonDoubleOuts(left, darts - 1, nums[nums.index(d):])

    known[key] = nCount

    return nCount


def getDoubleOuts(n, nums, doubles):
    # Get possible double outs
    nCount = 0
    for left, d in [(n - d[0], d) for d in doubles if d[0] <= n]:
        if left == 0:
            nCount += 1
        else:
            nCount += getNonDoubleOuts(left, 2, nums)
    return nCount


def challenge109():
    """ challenge109 """
    nums = [(x, x) for x in range(1, 21)]
    nums += [(x*2, x) for x in range(1, 21)]
    nums += [(x*3, x) for x in range(1, 21)]
    nums += [(25, 25), (50, 25)]
    nums.sort()

    doubles = [(x*2, x) for x in range(1, 21)] + [(50, 25)]

    nCount = 0
    for out in range(1, 100):
        outs = getDoubleOuts(out, nums, doubles)
        nCount += outs

    return nCount
