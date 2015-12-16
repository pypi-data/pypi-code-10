


class ContextMixin(object):
    """Defines a ``GET`` method that invokes :meth:`get_rendering_context()`
    and returns its result to the client.
    """

    def get_rendering_context(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must override this method.")
