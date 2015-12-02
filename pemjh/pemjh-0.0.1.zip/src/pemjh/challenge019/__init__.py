""" Challenge019 """


def is_leap_year(year):
    """
    Get whether or not the year is a leap year.
    >>> is_leap_year(1900)
    False
    >>> is_leap_year(2000)
    True
    >>> is_leap_year(1999)
    False
    >>> is_leap_year(2004)
    True
    """
    return ((not year % 100) and (not year % 400)) or \
        ((year % 100 != 0) and (not year % 4))


def get_year_days(year):
    """
    Get the number of days in the year.
    >>> get_year_days(1900)
    365
    >>> get_year_days(2000)
    366
    >>> get_year_days(1999)
    365
    >>> get_year_days(2004)
    366
    """
    if is_leap_year(year):
        return 366
    else:
        return 365


def get_first_january(year):
    """
    Get the day of the week of the 1st January this year
    >>> get_first_january(1900)
    1
    """
    total_days = 1
    for i in xrange(1900, year):
        total_days += get_year_days(i)
    return total_days % 7


def month_start_days(year):
    """ Generate the day of the week for a year.
    >>> list(month_start_days(1900))
    [1, 4, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6]
    """
    # Get the 1st of january
    day = get_first_january(year)
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]
    if is_leap_year(year):
        month_lengths[1] = 29

    yield day
    for month in month_lengths:
        day += month
        day = day % 7
        yield day


def challenge019():
    """ challenge019 """
    # Loop through years
    total_days = 0
    for year in xrange(1901, 2001):
        # Loop through the first days of the months for the year
        for day in month_start_days(year):
            if day == 0:
                total_days += 1

    return total_days
