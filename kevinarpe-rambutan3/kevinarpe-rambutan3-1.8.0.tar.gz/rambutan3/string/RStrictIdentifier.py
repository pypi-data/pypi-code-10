import re

from rambutan3.string.RMessageText import RMessageText
from rambutan3.string.RPatternText import RPatternText


class RStrictIdentifier(RPatternText):
    """
    Wraps a {@link str} value that is a valid C programming language identifier:
    (1) Starts with [A-Za-z_]
    (2) Followed by zero or more [0-9A-Za-z_]

    Examples: email_address, telephone_number123, or __something_very_private

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)
    @see RIdentifier
    """

    __REGEX_PATTERN = re.compile(r'^[A-Za-z_][0-9A-Za-z_]*$')
    __HUMAN_READABLE_HINT = RMessageText('strict identifier, e.g., ClassName or var_name3')

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
