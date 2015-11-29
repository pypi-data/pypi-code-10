from rambutan3.container.RAbstractForwardingDict import RAbstractForwardingDict
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER


# noinspection PyAbstractClass
class RAbstractForwardingTypedDict(RAbstractForwardingDict):

    @check_args
    def __init__(self: SELF(),
                 key_matcher: TYPE_MATCHER | NONE=None,
                 value_matcher: TYPE_MATCHER | NONE=None):
        """
        @param key_matcher
               optional if value_matcher is not None
        @param value_matcher
               optional if key_matcher is not None
        """
        super().__init__()
        if (key_matcher is None) and (value_matcher is None):
            raise ValueError("Both key_matcher and value_matcher are None")
        self.__key_matcher = key_matcher
        """:type: RAbstractTypeMatcher"""
        self.__value_matcher = value_matcher
        """:type: RAbstractTypeMatcher"""

    @property
    def key_matcher(self):
        return self.__key_matcher

    @property
    def value_matcher(self):
        return self.__value_matcher

    def __setitem__(self, key, value):
        if self.__key_matcher is not None:
            self.__key_matcher.check_arg(key, "Key {}='{}': ", type(key).__name__, key)

        if self.__value_matcher is not None:
            self.__value_matcher.check_arg(value, "(Key: Value): ({}='{}': {}='{}'): ",
                                           type(key).__name__, key, type(value).__name__, value)

        self._delegate[key] = value
