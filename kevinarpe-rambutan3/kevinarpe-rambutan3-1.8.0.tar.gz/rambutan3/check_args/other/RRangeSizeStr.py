from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.RInstanceMatcher import RInstanceMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.collection.RRangeSizeMatcher import RRangeSizeMatcher


class RRangeSizeStr(RAbstractTypeMatcher):
    """
    This class is fully tested.
    """

    __STR_MATCHER = RInstanceMatcher(str)

    # noinspection PyMissingConstructor
    def __init__(self, *, min_size: int=-1, max_size: int=-1):
        self.__range_size_matcher = RRangeSizeMatcher(min_size=min_size, max_size=max_size)

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__STR_MATCHER.matches(value, matcher_error):
            return False

        x = self.__range_size_matcher.matches(value, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeStr):
            return False

        x = (self.__range_size_matcher == other.__range_size_matcher)

        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__range_size_matcher)
        return x

    # @override
    def __str__(self) -> str:
        x = str(self.__STR_MATCHER) + str(self.__range_size_matcher)
        return x
