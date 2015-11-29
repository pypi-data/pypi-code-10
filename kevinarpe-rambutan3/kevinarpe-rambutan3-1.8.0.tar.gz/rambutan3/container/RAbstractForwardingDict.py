from collections.abc import MutableMapping
from abc import abstractmethod
from rambutan3.container.RDict import RDict


class RAbstractForwardingDict(MutableMapping, RDict):

    @property
    @abstractmethod
    def _delegate(self) -> dict:
        """Do not forget to include decorator @property in the overriding subclasses!"""
        raise NotImplementedError()

    def __getitem__(self, key):
        if key in self._delegate:
            x = self._delegate[key]
            return x
        if hasattr(self.__class__, "__missing__"):
            # noinspection PyUnresolvedReferences
            x = self.__class__.__missing__(self, key)
            return x
        raise KeyError(key)

    def __iter__(self):
        x = iter(self._delegate)
        return x

    def __len__(self):
        x = len(self._delegate)
        return x

    # Note that __missing__() is not called for any operations besides __getitem__().
    # Ref: https://docs.python.org/3/library/collections.html#collections.defaultdict
    def __contains__(self, key):
        x = key in self._delegate
        return x

    def __setitem__(self, key, value):
        self._delegate[key] = value

    def __delitem__(self, key):
        del self._delegate[key]

    def __repr__(self):
        x = repr(self._delegate)
        return x

    def __str__(self):
        x = str(self._delegate)
        return x
