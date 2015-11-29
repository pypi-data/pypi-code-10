from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.iter.RIterableOfMatcher import RIterableOfMatcher
from rambutan3.check_args.set.RRangeSizeSetMatcher import RRangeSizeSetMatcher
from rambutan3.check_args.set.RSetEnum import RSetEnum


class RRangeSizeSetOfMatcher(RRangeSizeSetMatcher):

    def __init__(self,
                 set_enum: RSetEnum,
                 element_matcher: RAbstractTypeMatcher,
                 *,
                 min_size: int=-1,
                 max_size: int=-1):
        super().__init__(set_enum, min_size=min_size, max_size=max_size)
        RArgs.check_is_instance(element_matcher, RAbstractTypeMatcher, "element_matcher")
        self.__element_matcher = element_matcher

    # @override
    def matches(self, set_: set, matcher_error: RTypeMatcherError=None) -> bool:
        if not super().matches(set_, matcher_error):
            return False

        x = RIterableOfMatcher.core_matches(set_, self.__element_matcher, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RRangeSizeSetOfMatcher):
            return False
        if not super().__eq__(other):
            return False
        x = (self.__element_matcher == other.__element_matcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        super_hash = super().__hash__()
        self_hash = hash(self.__element_matcher)
        x = super_hash ^ self_hash
        return x

    # @override
    def __str__(self):
        x = "{} of [{}]".format(super().__str__(), self.__element_matcher)
        return x
