from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.iter.RIterableOfMatcher import RIterableOfMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum
from rambutan3.check_args.seq.RSequenceMatcher import RSequenceMatcher


class RSequenceOfMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, seq_enum: RSequenceEnum, element_matcher: RAbstractTypeMatcher):
        self.__seq_matcher = RSequenceMatcher(seq_enum)
        RArgs.check_is_instance(element_matcher, RAbstractTypeMatcher, "element_matcher")
        self.__element_matcher = element_matcher

    # @override
    def matches(self, seq, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__seq_matcher.matches(seq, matcher_error):
            return False

        x = RIterableOfMatcher.core_matches(seq, self.__element_matcher, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RSequenceOfMatcher):
            return False

        if not self.__seq_matcher.__eq__(other.__seq_matcher):
            return False

        x = (self.__element_matcher == other.__element_matcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__seq_matcher, self.__element_matcher))
        return x

    # @override
    def __str__(self):
        x = "{} of [{}]".format(self.__seq_matcher, self.__element_matcher)
        return x
