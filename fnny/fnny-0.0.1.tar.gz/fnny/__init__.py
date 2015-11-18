
__all__ = ["pluck", "method", "partial"]
__version__ = '0.0.1'


class _PluckFactory(object):
    def __getattr__(self, name):
        def fn(thing):
            return getattr(thing, name)
        return fn


class _MethodFactory(object):
    def __getattr__(self, name):
        def fn(thing):
            # TODO: merge this into Partial somehow?
            return getattr(thing, name)()
        return fn


class _PartialFactory(object):
    def __getattr__(self, name):
        """ get a thing that passes args down """
        def partial_fn(*args, **kwargs):
            def fn(thing):
                return getattr(thing, name)(*args, **kwargs)
            return fn
        return partial_fn


pluck = _PluckFactory()
method = _MethodFactory()
partial = _PartialFactory()
