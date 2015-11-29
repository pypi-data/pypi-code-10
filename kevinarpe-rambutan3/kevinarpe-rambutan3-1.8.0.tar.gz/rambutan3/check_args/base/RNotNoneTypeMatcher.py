from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RNotNoneTypeMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        pass

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        x = value is not None

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __eq__(self, other) -> bool:
        x = isinstance(other, RNotNoneTypeMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        x = super(object, self).__hash__()
        return x

    # @override
    def __str__(self):
        return 'not None'
