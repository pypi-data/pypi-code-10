""" Challenge061 """
from itertools import chain


def has_duplicates(nums):
    """ Check whether the collection has duplicates """
    return len(nums) != len(set(nums))


def each_in_list(nums, lists):
    """ Check if all numbers are found in different lists """
    if len(nums) == 0:
        return True

    # Get the first list
    first_list = lists[0]
    # Cycle through nums
    for num in nums:
        # if the number is in the list
        if num in first_list:
            # Are the other numbers in the other lists?
            new_nums = [m for m in nums if m != num]
            new_lists = [k for k in lists if k != first_list]
            if each_in_list(new_nums, new_lists):
                return True

    return False


def challenge061():
    """ challenge061 """
    # Answer must lie between 1000 and 9999
    # Numbers cannot have the 3rd digit as 0

    all_lists = list()

    # Get all triangular numbers
    tri = list([n * (n + 1) / 2 for n in xrange(45, 141)])
    all_lists.append(tri)

    # Get all square numbers
    sq_nums = list([n**2 for n in xrange(32, 100)])
    all_lists.append(sq_nums)

    # Get all Pentagonal numbers
    pent = list([n * (3 * n - 1) / 2 for n in xrange(26, 82)])
    all_lists.append(pent)

    # Get all Hexagonal numbers
    hex_nums = list([n * (2 * n - 1) for n in xrange(23, 70)])
    all_lists.append(hex_nums)

    # Get all Heptagonal numbers
    hept = list([n * (5 * n - 3) / 2 for n in xrange(21, 64)])
    all_lists.append(hept)

    # Get all Octogonal numbers
    oct_nums = list([n * (3 * n - 2) for n in xrange(19, 59)])
    all_lists.append(oct_nums)

    # Get set of all known numbers
    all_nums = set(chain(tri, sq_nums, pent, hex_nums, hept, oct_nums))
    prefixes = dict()
    for num in all_nums:
        prefix = str(num)[:2]
        if prefix in prefixes:
            prefixes[prefix].add(num)
        else:
            prefixes[prefix] = set([num])
    # Remove any that could not cycle
    for num in all_nums:
        suffix = str(num)[2:]
        prefix = str(num)[:2]
        if suffix not in prefixes or (suffix == prefix):
            # Remove self
            prefixes[prefix].remove(num)
            for check_list in all_lists:
                if num in check_list:
                    check_list.remove(num)
    all_nums = None

    # Cycle through oct numbers (since they must occur)
    for num1 in oct_nums:
        # Get all possible number 2s
        num2s = prefixes[str(num1)[2:]]
        for num2 in num2s:
            # Get all possible number 3s
            num3s = prefixes[str(num2)[2:]]
            for num3 in num3s:
                # Get all possible number 4s
                num4s = prefixes[str(num3)[2:]]
                for num4 in num4s:
                    # Get all possible number 5s
                    num5s = prefixes[str(num4)[2:]]
                    for num5 in num5s:
                        # Get all possible number 6s
                        num6s = prefixes[str(num5)[2:]]
                        for num6 in num6s:
                            # Get all possible number 7/1s
                            num7s = prefixes[str(num6)[2:]]
                            for num7 in num7s:
                                if num1 == num7:
                                    potential = [num1,
                                                 num2,
                                                 num3,
                                                 num4,
                                                 num5,
                                                 num6]
                                    if not has_duplicates(potential):
                                        if each_in_list(potential, all_lists):
                                            return sum(potential)
