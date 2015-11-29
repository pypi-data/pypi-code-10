from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.SUBCLASS_OF import SUBCLASS_OF
from rambutan3.container.RAbstractForwardingDict import RAbstractForwardingDict
from rambutan3.enumeration.RTypedEnum import RTypedEnum


# noinspection PyAbstractClass
class RAbstractForwardingTypedEnumDict(RAbstractForwardingDict):

    @check_args
    def __init__(self: SELF(), key_type: SUBCLASS_OF(RTypedEnum)):
        super().__init__()
        self.__key_matcher = INSTANCE_OF(key_type)

    def __setitem__(self, key: RTypedEnum, value):
        self.__key_matcher.check_arg(key, "Key '{}.{}': ", type(key).__name__, key)
        key.value.check_arg(value, "(Key: Value): ('{}.{}': {}='{}'): ",
                            type(key).__name__, key, type(value).__name__, value)
        super().__setitem__(key, value)
