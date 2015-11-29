from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.DICT import DICT
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.SUBCLASS_OF import SUBCLASS_OF
from rambutan3.container.RAbstractForwardingTypedEnumDict import RAbstractForwardingTypedEnumDict
from rambutan3.enumeration.RTypedEnum import RTypedEnum


class RTypedEnumDict(RAbstractForwardingTypedEnumDict):

    @check_args
    def __init__(self: SELF(), key_type: SUBCLASS_OF(RTypedEnum), dictionary: DICT | NONE=None):
        super().__init__(key_type)
        self.__dict = {}
        if dictionary:  # not None and not empty
            self.update(dictionary)

    # @overrides
    @property
    def _delegate(self) -> dict:
        return self.__dict
