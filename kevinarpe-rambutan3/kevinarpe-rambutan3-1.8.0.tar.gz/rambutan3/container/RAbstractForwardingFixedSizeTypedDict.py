from rambutan3.container.RAbstractForwardingTypedDict import RAbstractForwardingTypedDict


# noinspection PyAbstractClass
class RAbstractForwardingFixedSizeTypedDict(RAbstractForwardingTypedDict):

    @property
    def _blocked_attribute(self):
        raise AttributeError("Unmodifiable container")

    __delitem__ = pop = popitem = clear = _blocked_attribute
