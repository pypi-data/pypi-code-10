from rambutan3 import RArgs
from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RSubclassMatcher(RAbstractTypeMatcher):
    """Type and (sub)class matcher

    Example:
    class X: pass
    class Y(X): pass
    True : X is a subclass of X.
    True : Y is a subclass of X.
    False: X is a subclass of Y.

    TODO: This class is fully tested.

    @author Kevin Connor ARPE (kevinarpe@gmail.com)

    @see builtins#issubclass()
    """

    # noinspection PyMissingConstructor
    def __init__(self, class_or_type: type):
        # Intentional: Do not call super(RAbstractTypeMatcher, self).__init__()
        RArgs.check_is_instance(class_or_type, type, "class_or_type")
        self.__type = class_or_type

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        # TODO: Why the try-except here?  When does it throw?
        try:
            x = issubclass(value, self.__type)
        except Exception as e:
            x = False

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __eq__(self, other) -> bool:
        if not isinstance(other, RSubclassMatcher):
            return False

        x = (self.__type == other.__type)
        return x

    # @override
    def __hash__(self) -> int:
        x = hash(self.__type)
        return x

    # @override
    def __str__(self):
        x = "subclass of {}".format(self.__type.__name__)
        return x
