import enum
from collections.abc import Mapping, MutableMapping

from rambutan3.container.frozendict import frozendict
from rambutan3.container.hashabledict import hashabledict
from rambutan3.enumeration.REnum import REnum


@enum.unique
class RDictEnum(REnum):

    BUILTIN_DICT = (dict,)
    DICT = (dict, hashabledict, frozendict, Mapping, MutableMapping)
