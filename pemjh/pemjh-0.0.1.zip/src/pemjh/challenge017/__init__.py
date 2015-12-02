""" Challenge017 """


def get_number_length(number, known):
    """
    >>> get_number_length(1000, dict())
    'onethousand'
    >>> known = {0: '', 20: 'twenty', 1: 'one'}
    >>> get_number_length(21, known)
    'twentyone'
    """
    if number == 1000:
        return "onethousand"
    else:
        current = number

        number_representation = known[0]
        # If over one hundred then print the hundred section
        if current > 99:
            # Get the hundreds
            hundreds = current / 100
            # Add the hundreds string
            number_representation += known[hundreds] + "hundred"
            # Add "and" if the number is not an exact hundred
            if current % 100:
                number_representation += "and"
            # Remove the hundreds column for later processing
            current -= (hundreds * 100)

        # Is remainder already known
        if current in known:
            number_representation += known[current]
        else:
            # Get the tens
            tens = current / 10
            # Remove the tens column for later processing
            current -= (tens * 10)
            # Add the tens string
            number_representation += known[tens * 10]

            number_representation += known[current]

    known[number] = number_representation

    return number_representation


def challenge017():
    """ challenge017 """
    known = {0: "",
             1: "one",
             2: "two",
             3: "three",
             4: "four",
             5: "five",
             6: "six",
             7: "seven",
             8: "eight",
             9: "nine",
             10: "ten",
             11: "eleven",
             12: "twelve",
             13: "thirteen",
             14: "fourteen",
             15: "fifteen",
             16: "sixteen",
             17: "seventeen",
             18: "eighteen",
             19: "nineteen",
             20: "twenty",
             30: "thirty",
             40: "forty",
             50: "fifty",
             60: "sixty",
             70: "seventy",
             80: "eighty",
             90: "ninety"}

    complete = ""
    for i in range(1, 1001):
        complete += get_number_length(i, known)

    return len(complete)
