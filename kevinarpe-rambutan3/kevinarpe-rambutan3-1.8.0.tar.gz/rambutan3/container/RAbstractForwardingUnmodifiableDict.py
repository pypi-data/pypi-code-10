from collections.abc import Mapping
from abc import abstractmethod
from rambutan3.container.RDict import RDict


class RAbstractForwardingUnmodifiableDict(Mapping, RDict):

    @property
    def _blocked_attribute(self):
        raise AttributeError("Unmodifiable container")

    __setitem__ = __delitem__ = pop = popitem = clear = update = setdefault = _blocked_attribute

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

    def __repr__(self):
        x = repr(self._delegate)
        return x

    def __str__(self):
        x = str(self._delegate)
        return x
