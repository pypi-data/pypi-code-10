"""This module is fully tested."""


def is_iterable(value) -> bool:
    try:
        iter(value)
    except:
        return False

    # Special case: Almost no one expects type 'str' to iterable.
    x = not isinstance(value, str)
    return x


def make_iterable(value):
    if is_iterable(value):
        return value

    return (value,)
