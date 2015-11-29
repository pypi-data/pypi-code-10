from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceOfMatcher import RSequenceOfMatcher
from rambutan3.check_args.seq.RUniqueSequenceMatcher import RUniqueSequenceMatcher


class RUniqueSequenceOfMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, seq_enum: RSequenceEnum, element_matcher: RAbstractTypeMatcher):
        self.__seq_of_matcher = RSequenceOfMatcher(seq_enum, element_matcher)

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__seq_of_matcher.matches(seq, matcher_error):
            return False

        x = RUniqueSequenceMatcher.core_matches(self, seq, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RUniqueSequenceOfMatcher):
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
