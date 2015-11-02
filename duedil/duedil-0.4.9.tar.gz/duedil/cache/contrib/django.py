
from dogpile.cache.api import CacheBackend, NO_VALUE
from dogpile.cache import register_backend
from django.core.cache import get_cache

register_backend("django_cache", "duedilv3.contrib.django", "DjangoCacheBackend")


class DjangoCacheBackend(CacheBackend):
    def __init__(self, arguments):
        django_cache_name = arguments.pop('cache_name', 'default')
        self.cache = get_cache(django_cache_name)

    def get(self, key):
        return self.cache.get(key, NO_VALUE)

    def set(self, key, value):
        self.cache.set(key, value, self.timeout)

    def delete(self, key):
        self.cache.delete(key)
