import enum
from rambutan3.enumeration.REnum import REnum


def is_absolute_pathname(pathname: str) -> bool:
    x = pathname.startswith('/')
    return x


def is_relative_pathname(pathname: str) -> bool:
    x = not pathname.startswith('/')
    return x


@enum.unique
class RFilePathTypeEnum(REnum):

    # Weird and crazy: Do not use function pointers directly.  It will not build the enum correctly.
    ABSOLUTE = (is_absolute_pathname,)
    RELATIVE = (is_relative_pathname,)
