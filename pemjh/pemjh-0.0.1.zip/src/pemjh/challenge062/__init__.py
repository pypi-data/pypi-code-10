""" Challenge062 """
import string


def challenge062():
    """ challenge062 """
    cubes = dict()

    num = 1
    while True:
        potential_answer = num**3
        # Convert to string
        cubed = str(potential_answer)
        # Sort
        cubed = list(cubed)
        cubed.sort()
        cubed = string.join(cubed, "")
        # Remove leading zeros
        cubed.lstrip("0")
        # Add to dictionary
        if cubed in cubes:
            lowest, num_cubes = cubes[cubed]
            lowest = lowest if lowest < potential_answer else potential_answer
            num_cubes += 1
            if num_cubes == 5:
                return lowest
            else:
                cubes[cubed] = [lowest, num_cubes]
        else:
            cubes[cubed] = [potential_answer, 1]

        num += 1
