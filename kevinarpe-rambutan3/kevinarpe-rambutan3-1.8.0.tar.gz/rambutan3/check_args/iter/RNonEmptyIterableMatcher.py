from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RNonEmptyIterableMatcher(RAbstractTypeMatcher):
    """Non-empty iterable instance matcher

    TODO: This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see RArgs#check_iterable_not_empty()
    """

    # noinspection PyMissingConstructor
    def __init__(self):
        # Intentional: Do not call super().__init__()
        pass

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        try:
            RArgs.check_iterable_not_empty(value, "value")
            x = True
        except Exception as e:
            x = False

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __eq__(self, other) -> bool:
        x = isinstance(other, RNonEmptyIterableMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Stateless object -> Return const
        return 1

    # @override
    def __str__(self) -> str:
        return "non-empty iterable"
