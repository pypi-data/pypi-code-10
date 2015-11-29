from collections.abc import Set
from abc import abstractmethod
from rambutan3.container.RSet import RSet


class RAbstractForwardingUnmodifiableSet(Set, RSet):

    @property
    def _blocked_attribute(self):
        raise AttributeError("Unmodifiable container")

    __ior__ = __iand__ = __ixor__ = __isub__ = _blocked_attribute
    add = discard = remove = pop = clear = _blocked_attribute

    @property
    @abstractmethod
    def _delegate(self) -> set:
        """Do not forget to include decorator @property in the overriding subclasses!"""
        raise NotImplementedError()

    def __contains__(self, value):
        x = value in self._delegate
        return x

    def __iter__(self):
        x = iter(self._delegate)
        return x

    def __len__(self):
        x = len(self._delegate)
        return x

    def __repr__(self):
        x = repr(self._delegate)
        return x

    def __str__(self):
        x = str(self._delegate)
        return x
