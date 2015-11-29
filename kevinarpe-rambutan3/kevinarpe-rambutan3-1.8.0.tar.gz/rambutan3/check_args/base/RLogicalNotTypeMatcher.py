from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RLogicalNotTypeMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self, delegate: RAbstractTypeMatcher):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        RArgs.check_is_instance(delegate, RAbstractTypeMatcher, "delegate")
        self.__delegate = delegate

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        # Probably there is a bug here.  Not sure whether or not to pass matcher_error.
        x = self.__delegate.matches(value, matcher_error)
        y = not x

        if not y and matcher_error:
            matcher_error.add_failed_match(self, value)

        return y

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RLogicalNotTypeMatcher):
            return False

        x = (self.__delegate == other.__delegate)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__delegate)
        return x

    # @override
    def __str__(self):
        x = 'not {}'.format(self.__delegate)
        return x
