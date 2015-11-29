from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.enumeration.REnum import REnum
from rambutan3.check_args.RCheckArgs import check_args
from rambutan3.check_args.annotation.SELF import SELF
from rambutan3.check_args.annotation.TYPE_MATCHER import TYPE_MATCHER


# Note: Do *not* annotate this class with @enum.unique.
# It will 'block' the check in subclasses using the same annotation.
class RTypedEnum(REnum):

    @check_args
    def __init__(self: SELF(), type_matcher: TYPE_MATCHER):
        """Argument {@code type_matcher} is unused in this ctor (except for validation via
        {@link RCheckArgs#check_args}), but automagically assigned to property {@link Enum#value}.
        """
        super().__init__()

    # @overrides
    @property
    def value(self) -> RAbstractTypeMatcher:
        x = super().value
        return x
