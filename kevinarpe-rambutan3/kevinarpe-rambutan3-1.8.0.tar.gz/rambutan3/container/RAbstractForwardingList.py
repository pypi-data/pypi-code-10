from collections.abc import MutableSequence
from abc import abstractmethod
from rambutan3.container.RList import RList


class RAbstractForwardingList(MutableSequence, RList):

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

    def __setitem__(self, index, value):
        self._delegate[index] = value

    def __delitem__(self, index):
        del self._delegate[index]

    def insert(self, index, value):
        self._delegate.insert(index, value)

    def __repr__(self):
        x = repr(self._delegate)
        return x

    def __str__(self):
        x = str(self._delegate)
        return x
