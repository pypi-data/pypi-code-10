from collections.abc import MutableSet
from abc import abstractmethod
from rambutan3.container.RSet import RSet


class RAbstractForwardingSet(MutableSet, RSet):

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

    def add(self, value):
        self._delegate.add(value)

    def discard(self, value):
        self._delegate.discard(value)

    def __repr__(self):
        x = repr(self._delegate)
        return x

    def __str__(self):
        x = str(self._delegate)
        return x
