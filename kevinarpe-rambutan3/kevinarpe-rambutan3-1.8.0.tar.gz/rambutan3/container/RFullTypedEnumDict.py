from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.DICT import DICT
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.SUBCLASS_OF import SUBCLASS_OF
from rambutan3.container.RAbstractForwardingFixedSizeTypedEnumDict import RAbstractForwardingFixedSizeTypedEnumDict
from rambutan3.container.RFullEnumKeyTypedDict import RFullEnumKeyTypedDict
from rambutan3.enumeration.RTypedEnum import RTypedEnum


class RFullTypedEnumDict(RAbstractForwardingFixedSizeTypedEnumDict):
    """Dictionary with checked {@link RTypedEnum} keys and values,
    and guaranteed to always have all enum members as keys.
    Values can change, but keys cannot be deleted, or added.
    """

    @check_args
    def __init__(self: SELF(), *, key_type: SUBCLASS_OF(RTypedEnum), dictionary: DICT):
        """
        @param key_type
               subclass of {@link RTypedEnum} used for key matcher
        @param dictionary
               initial values

        @throws ValueError
                if {@code dictionary} is missing any enum members
        """
        super().__init__(key_type)
        RFullEnumKeyTypedDict.static_check_missing_enum_keys(key_type, dictionary)
        self.__dict = {}
        self.update(dictionary)

    # @overrides
    @property
    def _delegate(self) -> dict:
        return self.__dict
