from decimal import Decimal

map_ones = {
    0: "",
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
}

map_tens = {
    10: "Ten",
    11: "Eleven",
    12: "Twelve",
    13: "Thirteen",
    14: "Fourteen",
    15: "Fifteen",
    16: "Sixteen",
    17: "Seventeen",
    18: "Eighteen",
    19: "Nineteen",
}

map_tenths = {
    2: "Twenty",
    3: "Thirty",
    4: "Forty",
    5: "Fifty",
    6: "Sixty",
    7: "Seventy",
    8: "Eighty",
    9: "Ninety",
}


def convert_ones(num):
    """
    Convert ones number to word.

    Parameters
    ----------
    num: int
        Single digit integer number
    """
    if len(str(num)) > 1:
        raise Exception("Must have at most 1 digit")
    num = int(num)
    return map_ones[num]


def convert_tenths(num):
    """
    Convert tenths number to word.

    Parameters
    ----------
    num: int
        Double digit integer number
    """
    if len(str(num)) > 2:
        raise Exception("Must have at most 2 digits")

    num = int(num)
    bases = ""

    # less than 10
    if num < 10:
        return map_ones[num]

    # 10-19
    if 10 <= num < 20:
        return map_tens[num]

    # 20-99
    first_num = map_tenths[int(str(num)[0])]
    second_num = map_ones[int(str(num)[1])]

    if not second_num:
        return first_num
    return first_num + " " + second_num


def get_dollar(hundredth, tenth, one, base):
    """
    Given hundredth, tenth and one integer number for base (e.g. Billion, Million), return converted word

    Parameters
    ----------
    hundredth: int
        Hundredth number
    tenth: int
        Tenth number
    one: int
        One number
    base: string
        Base value
    """
    dollar_word = ""
    if hundredth:
        dollar_word += "{0} Hundred".format(convert_ones(hundredth))

    # Add "And" if there's numbers after hundredths
    if hundredth and (tenth or one):
        dollar_word += " And "

    if tenth or one:
        dollar_word += "{0}".format(convert_tenths(int(str(tenth) + str(one))))

    if base:
        dollar_word += " {0}".format(base)
    return dollar_word


def get_billion(hundredth, tenth, one):
    return get_dollar(hundredth, tenth, one, "Billion")


def get_million(hundredth, tenth, one):
    return get_dollar(hundredth, tenth, one, "Million")


def get_thousand(hundredth, tenth, one):
    return get_dollar(hundredth, tenth, one, "Thousand")


def get_one(hundredth, tenth, one):
    return get_dollar(hundredth, tenth, one, "")


def get_cent(tenth, one):
    """
    Given tenth and one integer number (for cent), return converted word

    Parameters
    ----------
    tenth: int
        Tenth number
    one: int
        One number
    """
    cent_word = ""
    if tenth or one:
        cent_word += "{0}".format(convert_tenths(int(str(tenth) + str(one))))

    if cent_word:
        cent_word = "Cents {0} ".format(cent_word)
    return cent_word


def get_index(val, index, default=0):
    try:
        return val[index]
    except IndexError:
        return default


def extract(num):
    """
    Given a max 3 character number, extract and return hundredth, tenth and one value

    Parameters
    ----------
    num: string
        Number in string

    Return
    ----------
    hundredth: int
        Hundredth number
    tenth: int
        Tenth number
    one: int
        One number
    """
    hundredth = 0
    tenth = 0
    one = 0
    if len(num) == 3:
        hundredth, tenth, one = int(num[0]), int(num[1]), int(num[2])

    if len(num) == 2:
        tenth, one = int(num[0]), int(num[1])

    if len(num) == 1:
        one = int(num[0])

    return hundredth, tenth, one


def generate_dollar_word(num):
    """
    Generate word for dollar

    Parameters
    ----------
    num: string
        Dollar number in string
    """
    word = ""

    # at least 1 billion
    if len(num) > 9:
        billion_num = int(num[0:(len(num)-9)])
        num = str(int(num) - (billion_num*int(1e9)))
        hundredth, tenth, one = extract(str(billion_num))
        word += "{0} ".format(get_billion(hundredth, tenth, one))

    # at least 1 million
    if len(num) > 6:
        million_num = int(num[0:(len(num)-6)])
        num = str(int(num) - (million_num*int(1e6)))
        hundredth, tenth, one = extract(str(million_num))
        word += "{0} ".format(get_million(hundredth, tenth, one))

    # at least 1 thousand
    if len(num) > 3:
        thousand_num = int(num[0:(len(num)-3)])
        num = str(int(num) - (thousand_num*int(1e3)))
        hundredth, tenth, one = extract(str(thousand_num))
        word += "{0} ".format(get_thousand(hundredth, tenth, one))

    # at least 1
    if int(num) and len(num) > 0:
        one_num = int(num[0:len(num)])
        num = str(int(num) - one_num)
        hundredth, tenth, one = extract(str(one_num))
        word += "{0} ".format(get_one(hundredth, tenth, one))
    return word


def generate_cent_word(num):
    """
    Generate word for cent

    Parameters
    ----------
    num: string
        Cent number in string
    """
    word = ""
    hundredth, tenth, one = extract(str(num))
    word += get_cent(tenth, one)
    return word


def validate(amt):
    # amt MUST be in string to avoid accidental round off
    if Decimal(amt) > Decimal(str(1e11)):
        raise Exception("Please enter an amount smaller than 100 billion")

    if len(get_index(amt.split('.'), 1, "")) > 2:
        raise Exception("Please enter an amount within 2 decimal place")


def generate_word(amt):
    # remove commas and spaces from word
    amt = amt.replace(",", "").replace(" ", "")
    validate(amt)

    amt = '{0:.2f}'.format(Decimal(amt))
    amt_list = amt.split('.')
    dollar_amt = get_index(amt_list, 0)
    cent_amt = get_index(amt_list, 1)

    dollar_word = generate_dollar_word(dollar_amt)
    cent_word = generate_cent_word(cent_amt)

    if not dollar_word:
        return cent_word + "Only"

    if not cent_word:
        return dollar_word + "Only"

    return dollar_word + "And " + cent_word + "Only"
