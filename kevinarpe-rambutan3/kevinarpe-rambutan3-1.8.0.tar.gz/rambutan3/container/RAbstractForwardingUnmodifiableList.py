from collections.abc import Sequence
from abc import abstractmethod
from rambutan3.container.RList import RList


class RAbstractForwardingUnmodifiableList(Sequence, RList):

    @property
    def _blocked_attribute(self):
        raise AttributeError("Unmodifiable container")

    __setitem__ = __delitem__ = __iadd__ = _blocked_attribute
    insert = append = clear = reverse = extend = pop = remove = _blocked_attribute

    @property
    @abstractmethod
    def _delegate(self) -> list:
        """Do not forget to include decorator @property in the overriding subclasses!"""
        raise NotImplementedError()

    def __getitem__(self, index):
        x = self._delegate[index]
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
