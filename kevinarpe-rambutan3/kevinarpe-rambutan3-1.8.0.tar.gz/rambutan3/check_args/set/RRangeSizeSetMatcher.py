from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.collection.RRangeSizeMatcher import RRangeSizeMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum
from rambutan3.check_args.set.RSetMatcher import RSetMatcher


class RRangeSizeSetMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, set_enum: RSetEnum, *, min_size: int=-1, max_size: int=-1):
        self.__set_matcher = RSetMatcher(set_enum)
        self.__range_size_matcher = RRangeSizeMatcher(min_size=min_size, max_size=max_size)

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__set_matcher.matches(value, matcher_error):
            return False

        x = self.__range_size_matcher.matches(value, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeSetMatcher):
            return False

        x = ((self.__set_matcher == other.__set_matcher)
             and (self.__range_size_matcher == other.__range_size_matcher))

        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__set_matcher, self.__range_size_matcher))
        return x

    # @override
    def __str__(self) -> str:
        x = str(self.__set_matcher) + str(self.__range_size_matcher)
        return x
