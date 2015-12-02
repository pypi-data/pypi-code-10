""" Challenge004 """


def challenge004():
    """
    Decrement number 1 from 990 in steps of 11
    Making the assumption that the number will be 6 figures and..
    all even numbered palindromic numbers are divisible by 11
    """
    eleven_num = 990
    highest_palindrome = 0

    while eleven_num > 99:
        # Decrement from 999 to 100
        second_num = 999

        while second_num > 99:
            # Get the potential palindrome
            potential_palindrome = eleven_num * second_num

            # If the number is lower than or equal to..
            # the highest_palindrome then break
            if potential_palindrome <= highest_palindrome:
                break

            # Convert the potential to a string
            forward = str(potential_palindrome)

            if forward == forward[::-1]:
                highest_palindrome = potential_palindrome
                break

            second_num -= 1

        eleven_num -= 11

    return highest_palindrome
