from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.iter.RIterableOfMatcher import RIterableOfMatcher
from rambutan3.check_args.iter.RNonEmptyIterableMatcher import RNonEmptyIterableMatcher


class RNonEmptyIterableOfMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, element_matcher: RAbstractTypeMatcher):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        self.__delegate = RNonEmptyIterableMatcher()
        RArgs.check_is_instance(element_matcher, RAbstractTypeMatcher, "element_matcher")
        self.__element_matcher = element_matcher

    # @override
    def matches(self, iterable, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__delegate.matches(iterable, matcher_error):
            return False

        x = RIterableOfMatcher.core_matches(iterable, self.__element_matcher, matcher_error)
        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RNonEmptyIterableOfMatcher):
            return False
        x = (self.__element_matcher == other.__element_matcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Ref: http://stackoverflow.com/questions/29435556/how-to-combine-hash-codes-in-in-python3
        delegate_hash = hash(self.__delegate)
        self_hash = hash(self.__element_matcher)
        x = delegate_hash ^ self_hash
        return x

    # @override
    def __str__(self) -> str:
        x = "non-empty iterable of [{}]".format(self.__element_matcher)
        return x
