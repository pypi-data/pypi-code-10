from abc import abstractmethod

from rambutan3.check_args.base.RAbstractTypeMatcher import RAbstractTypeMatcher
from rambutan3.check_args.base.traverse.RTypeMatcherError import RTypeMatcherError


class RAbstractForwardingTypeMatcher(RAbstractTypeMatcher):

    # noinspection PyMissingConstructor
    def __init__(self):
        raise NotImplementedError('Internal error: Do not call this constructor')

    @property
    @abstractmethod
    def _delegate(self) -> RAbstractTypeMatcher:
        """Do not forget to include decorator @property in the overriding subclasses!"""
        raise NotImplementedError()

    # @override
    def matches(self, value, matcher_error: RTypeMatcherError=None) -> bool:
        x = self._delegate.matches(value, matcher_error)
        return x

    # # @override
    # def check_arg(self, value, arg_name: str, *arg_name_format_args):
    #     self._delegate.check_arg(value, arg_name, *arg_name_format_args)

    # Leave this code for history.
    # Disabled during testing as this causes bugs.
    # # @override
    # def __or__(self, other: RAbstractTypeMatcher) -> RAbstractTypeMatcher:
    #     x = self._delegate.__or__(other)
    #     return x

    # @override
    def __eq__(self, other: RAbstractTypeMatcher) -> bool:
        if not isinstance(other, type(self)):
            return False

        x = self._delegate.__eq__(other._delegate)
        return x

    # Leave this code for history.
    # Disabled during testing as this causes bugs.
    # # @override
    # def __ne__(self, other: RAbstractTypeMatcher) -> bool:
    #     if not isinstance(other, type(self)):
    #         return True
    #
    #     x = self._delegate.__ne__(other._delegate)
    #     return x

    # @override
    def __hash__(self) -> int:
        x = self._delegate.__hash__()
        return x

    # @override
    def __str__(self) -> str:
        x = self._delegate.__str__()
        return x
