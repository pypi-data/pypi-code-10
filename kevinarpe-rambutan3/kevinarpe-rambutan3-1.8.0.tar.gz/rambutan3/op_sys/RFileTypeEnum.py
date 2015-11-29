import enum
import stat
from rambutan3.enumeration.REnum import REnum


@enum.unique
class RFileTypeEnum(REnum):

    # Weird and crazy: Do not use function pointers directly.  It will not build the enum correctly.
    DIRECTORY = (stat.S_ISDIR,)
    CHAR_SPECIAL_DEVICE = (stat.S_ISCHR,)
    BLOCK_SPECIAL_DEVICE = (stat.S_ISBLK,)
    REGULAR_FILE = (stat.S_ISREG,)
    NAMED_PIPE = (stat.S_ISFIFO,)
    SYMBOLIC_LINK = (stat.S_ISLNK,)
    SOCKET = (stat.S_ISSOCK,)
    DOOR = (stat.S_ISDOOR,)
    EVENT_PORT = (stat.S_ISPORT,)
    WHITEOUT = (stat.S_ISWHT,)
