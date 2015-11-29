from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.collection.RRangeSizeMatcher import RRangeSizeMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceMatcher import RSequenceMatcher


class RRangeSizeSequenceMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, seq_enum: RSequenceEnum, *, min_size: int=-1, max_size: int=-1):
        self.__seq_matcher = RSequenceMatcher(seq_enum)
        self.__range_size_matcher = RRangeSizeMatcher(min_size=min_size, max_size=max_size)

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__seq_matcher.matches(value, matcher_error):
            return False

        x = self.__range_size_matcher.matches(value, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeSequenceMatcher):
            return False

        x = ((self.__seq_matcher == other.__seq_matcher)
             and (self.__range_size_matcher == other.__range_size_matcher))

        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__seq_matcher, self.__range_size_matcher))
        return x

    # @override
    def __str__(self) -> str:
        x = str(self.__seq_matcher) + str(self.__range_size_matcher)
        return x
