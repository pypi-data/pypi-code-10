import enum
from rambutan3.enumeration.REnum import REnum


@enum.unique
class RBinarySequenceEnum(REnum):

    BYTES = (bytes,)
    BYTEARRAY = (bytearray,)
    MEMORYVIEW = (memoryview,)
    BINARY_SEQUENCE = (bytes, bytearray, memoryview)
