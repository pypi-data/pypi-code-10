from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.DICT import DICT
from rambutan3.check_args.annotation.INSTANCE_OF import INSTANCE_OF
from rambutan3.check_args.annotation.NONE import NONE
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.SUBCLASS_OF import SUBCLASS_OF
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER
from rambutan3.container.RAbstractForwardingFixedSizeTypedDict import RAbstractForwardingFixedSizeTypedDict
from rambutan3.enumeration.REnum import REnum


class RFullEnumKeyTypedDict(RAbstractForwardingFixedSizeTypedDict):
    """Dictionary with checked {@link REnum} keys and guaranteed to always have all enum members as keys.
    Values can change, but keys cannot be deleted, or added.
    """

    @check_args
    def __init__(self: SELF(),
                 *,
                 key_type: SUBCLASS_OF(REnum),
                 value_matcher: TYPE_MATCHER | NONE=None,
                 dictionary: DICT):
        """
        @param key_type
               subclass of {@link REnum} used for key matcher
        @param value_matcher
               optional value matcher
        @param dictionary
               initial values

        @throws ValueError
                if {@code dictionary} is missing any enum members
        """
        key_matcher = INSTANCE_OF(key_type)
        super().__init__(key_matcher, value_matcher)
        self.static_check_missing_enum_keys(key_type, dictionary)
        self.__dict = {}
        self.update(dictionary)

    @staticmethod
    def static_check_missing_enum_keys(key_type: SUBCLASS_OF(REnum), dictionary: DICT):
        """
        @throws ValueError
                if {@code dictionary} is missing any enum members
        """
        enum_set = set(key_type.__members__.values())
        key_set = set(dictionary.keys())
        missing_enum_set = enum_set - key_set
        if missing_enum_set:
            join = ", ".join([x.name for x in missing_enum_set])
            raise ValueError("Missing keys from enum {}: {}".format(key_type.__name__, join))

    # @overrides
    @property
    def _delegate(self) -> dict:
        return self.__dict
