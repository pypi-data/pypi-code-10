from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RRangeSizeSequenceOfMatcher import RRangeSizeSequenceOfMatcher
from rambutan3.check_args.seq.RUniqueSequenceMatcher import RUniqueSequenceMatcher


class RRangeSizeUniqueSequenceOfMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self,
                 seq_enum: RSequenceEnum,
                 element_matcher: RAbstractTypeMatcher,
                 *,
                 min_size: int=-1,
                 max_size: int=-1):
        self.__seq_of_matcher = \
            RRangeSizeSequenceOfMatcher(seq_enum, element_matcher, min_size=min_size, max_size=max_size)

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__seq_of_matcher.matches(seq, matcher_error):
            return False

        x = RUniqueSequenceMatcher.core_matches(self, seq, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeUniqueSequenceOfMatcher):
            return False

        x = (self.__seq_of_matcher == other.__seq_of_matcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__seq_of_matcher)
        return x

    # @override
    def __str__(self):
        x = "unique {}".format(self.__seq_of_matcher)
        return x
