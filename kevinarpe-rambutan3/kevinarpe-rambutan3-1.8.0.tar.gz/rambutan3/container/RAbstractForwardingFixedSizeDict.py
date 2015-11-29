from rambutan3.container.RAbstractForwardingDict import RAbstractForwardingDict


# noinspection PyAbstractClass
class RAbstractForwardingFixedSizeDict(RAbstractForwardingDict):

    @property
    def _blocked_attribute(self):
        raise AttributeError("Unmodifiable container")

    __delitem__ = pop = popitem = clear = _blocked_attribute
