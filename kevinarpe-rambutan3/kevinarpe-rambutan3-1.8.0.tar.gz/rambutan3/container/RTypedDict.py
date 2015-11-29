from rambutan3.container.RAbstractForwardingTypedDict import RAbstractForwardingTypedDict
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.DICT import DICT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER


class RTypedDict(RAbstractForwardingTypedDict):
    """A mutable dictionary subclass that restrict keys, values, or both by type matchers.

    This class is fully tested.
    """

    @check_args
    def __init__(self: SELF(),
                 key_matcher: TYPE_MATCHER | NONE=None,
                 value_matcher: TYPE_MATCHER | NONE=None,
                 dictionary: DICT | NONE=None):
        """
        @param key_matcher
               optional if value_matcher is not None
        @param value_matcher
               optional if key_matcher is not None
        @param dictionary
               optional; added to new dict, but subject to key_matcher and value_matcher restrictions
        """
        super().__init__(key_matcher, value_matcher)
        self.__dict = {}
        if dictionary:  # not None and not empty
            self.update(dictionary)

    # @overrides
    @property
    def _delegate(self) -> dict:
        return self.__dict
