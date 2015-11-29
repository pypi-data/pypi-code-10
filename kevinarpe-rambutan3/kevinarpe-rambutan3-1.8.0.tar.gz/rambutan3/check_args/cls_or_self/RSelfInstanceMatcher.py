from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError
from rambutan3.check_args.cls_or_self.RAbstractClassOrSelfInstanceMatcher import RAbstractClassOrSelfInstanceMatcher


class RSelfInstanceMatcher(RAbstractClassOrSelfInstanceMatcher):
    """Never use this class directly.  Instead, use: {@link SELF#SELF()}.

    Technically, this class is a delayed caller class lookup for {@link builtins#isinstance()}.
    """

    def __init__(self):
        super().__init__()

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        x = isinstance(value, self._caller_class)

        if not x and matcher_error:
            matcher_error.add_failed_match(self, value)

        return x

    # @override
    def __str__(self):
        x = "self: {}".format(self._caller_class.__name__)
        return x
