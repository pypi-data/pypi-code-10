import enum
from collections.abc import Sequence, MutableSequence
from collections import namedtuple

from rambutan3.enumeration.REnum import REnum


RSequenceEnumData = namedtuple('RSequenceEnum', ['allowed_type_tuple', 'not_allowed_type_tuple'])


@enum.unique
class RSequenceEnum(REnum):

    TUPLE = RSequenceEnumData(allowed_type_tuple=(tuple,), not_allowed_type_tuple=())
    LIST = RSequenceEnumData(allowed_type_tuple=(list,), not_allowed_type_tuple=())

    # Dreadfully, class 'str' extends 'Sequence'.  Do not allow!
    SEQUENCE = RSequenceEnumData(allowed_type_tuple=(tuple, Sequence, list, MutableSequence),
                                 not_allowed_type_tuple=(str,))
