from rambutan3.container.RAbstractForwardingTypedEnumDict import RAbstractForwardingTypedEnumDict


# noinspection PyAbstractClass
class RAbstractForwardingFixedSizeTypedEnumDict(RAbstractForwardingTypedEnumDict):

    @property
    def _blocked_attribute(self):
        raise AttributeError("Unmodifiable container")

    __delitem__ = pop = popitem = clear = _blocked_attribute
