from journaler.models import VALID_MEALS


def validate_rating(value):
    """
    Ensures value is an int between 1 and 5
    :param value:
        Hopefully something that can be turned into an int
        hopefully between 1 and 5
    :throws ValueError if the conditions are not met
    """
    # Yes I know this wont invalidate floats. Im ok with that
    int_value = int(value)
    if int_value < 1 or int_value > 5:
        raise ValueError("ratings must be between 1 and 5")


def validate_meal(value):
    """
    Ensures meal is on of the valid ones
    :param value:
        meal value
    :throws ValueError if meal is invalid
    """
    if value.lower() not in VALID_MEALS:
        raise ValueError("Meal must be one of {}".format(VALID_MEALS))
