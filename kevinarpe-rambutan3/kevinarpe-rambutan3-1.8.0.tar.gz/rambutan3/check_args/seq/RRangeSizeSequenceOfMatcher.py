from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.iter.RIterableOfMatcher import RIterableOfMatcher
from rambutan3.check_args.seq.RRangeSizeSequenceMatcher import RRangeSizeSequenceMatcher
from rambutan3.check_args.seq.RSequenceEnum import RSequenceEnum


class RRangeSizeSequenceOfMatcher(RAbstractTypeMatcher):
    """This class is fully tested."""

    # noinspection PyMissingConstructor
    def __init__(self,
                 seq_enum: RSequenceEnum,
                 element_matcher: RAbstractTypeMatcher,
                 *,
                 min_size: int=-1,
                 max_size: int=-1):
        self.__matcher = RRangeSizeSequenceMatcher(seq_enum, min_size=min_size, max_size=max_size)
        RArgs.check_is_instance(element_matcher, RAbstractTypeMatcher, "element_matcher")
        self.__element_matcher = element_matcher

    # @override
    def matches(self, collection, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__matcher.matches(collection, matcher_error):
            return False

        x = RIterableOfMatcher.core_matches(collection, self.__element_matcher, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeSequenceOfMatcher):
            return False

        if not self.__matcher == other.__matcher:
            return False

        x = (self.__element_matcher == other.__element_matcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash((self.__matcher, self.__element_matcher))
        return x

    # @override
    def __str__(self):
        x = "{} of [{}]".format(self.__matcher.__str__(), self.__element_matcher)
        return x
