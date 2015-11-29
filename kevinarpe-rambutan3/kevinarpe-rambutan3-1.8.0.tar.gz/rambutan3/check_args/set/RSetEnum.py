import enum
from collections.abc import Set, MutableSet

from rambutan3.container.hashableset import hashableset
from rambutan3.enumeration.REnum import REnum


@enum.unique
class RSetEnum(REnum):

    BUILTIN_SET = (set,)
    BUILTIN_FROZENSET = (frozenset,)
    SET = (set, hashableset, frozenset, Set, MutableSet)
