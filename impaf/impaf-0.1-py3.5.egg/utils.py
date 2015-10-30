def cached(fun):
    name = fun.__name__

    def wrapper(self, *args, **kwargs):
        if name not in self._cache:
            self._cache[name] = fun(self, *args, **kwargs)
        return self._cache[name]

    return wrapper
