import re

from rambutan3.string.RMessageText import RMessageText
from rambutan3.string.RPatternText import RPatternText


class RIdentifier(RPatternText):
    """
    Wraps a {@link str} value that is a reasonable identifier:
    One or more [0-9A-Za-z_-.=]

    No whitespace or silly special chars.  The list above may slowly expand in the future.

    Examples: email_address, telephone_number123, or __something_very_private, 3rd, a.b.c, small-size, pid=123

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)
    @see RStrictIdentifier
    """

    # Same as strict identifier, but allow: -, ., =
    # ... and leading digits
    __REGEX_PATTERN = re.compile(r'^[0-9A-Za-z_\-\.=]+$')
    __HUMAN_READABLE_HINT = \
        RMessageText('identifier, e.g., "ClassName", "var_name3", "a.b.c", "small-size", "3rd", "pid=123"')

    @classmethod
    def REGEX_PATTERN(cls):
        return cls.__REGEX_PATTERN

    @classmethod
    def HUMAN_READABLE_HINT(cls):
        return cls.__HUMAN_READABLE_HINT

    # noinspection PyMissingConstructor
    def __init__(self, value: str):
        # Insane: We call RPatternText.new() only to validate argument 'value'.
        # We do not save the result, and allow the implicit ctor to be called.
        # Magic!
        RPatternText.new(value, self.__REGEX_PATTERN, self.__HUMAN_READABLE_HINT)
        # Crazy, crazy, crazy.  Do not call super().__init__()!  No idea how this magic works.
