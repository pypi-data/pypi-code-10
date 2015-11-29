from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.base.traverse.RTypeMatcherTraversePathStepEnum import RTypeMatcherTraversePathStepEnum
from rambutan3.check_args.iter.RIterableMatcher import RIterableMatcher


class RIterableOfMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, element_matcher: RAbstractTypeMatcher):
        # Intentional: Do not call super().__init__()
        self.__delegate = RIterableMatcher()
        RArgs.check_is_instance(element_matcher, RAbstractTypeMatcher, "element_matcher")
        self.__element_matcher = element_matcher

    # @override
    def matches(self, iterable, matcher_error: RTypeMatcherError=None) -> bool:
        if not self.__delegate.matches(iterable, matcher_error):
            return False

        x = self.core_matches(iterable, self.__element_matcher, matcher_error)
        return x

    @classmethod
    def core_matches(cls,
                     iterable,
                     element_matcher: RAbstractTypeMatcher,
                     matcher_error: RTypeMatcherError=None) -> bool:

        x = all(element_matcher.matches(y, matcher_error) for y in iterable)

        if not x and matcher_error:
            # Slow path: Report errors here
            for index, value in enumerate(iterable):
                # Intentional: Do not pass matcher_error here.
                if not element_matcher.matches(value):
                    matcher_error.add_traverse_path_step(RTypeMatcherTraversePathStepEnum.Index, index)
                    break

        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RIterableOfMatcher):
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
        x = "iterable of [{}]".format(self.__element_matcher)
        return x
