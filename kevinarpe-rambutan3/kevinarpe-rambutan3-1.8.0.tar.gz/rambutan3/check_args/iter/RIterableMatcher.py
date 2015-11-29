from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RIterableMatcher(RAbstractTypeMatcher):
    """Iterable instance matcher

    This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see RArgs#is_iterable()
    """

    # noinspection PyMissingConstructor
    def __init__(self):
        # Intentional: Do not call super().__init__()
        pass

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        try:
            RArgs.check_is_iterable(value, "value")
            x = True
        except Exception as e:
            x = False

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __eq__(self, other) -> bool:
        x = isinstance(other, RIterableMatcher)
        return x

    # @override
    def __hash__(self) -> int:
        # Stateless object -> Return const
        return 1

    # @override
    def __str__(self) -> str:
        return "iterable"
