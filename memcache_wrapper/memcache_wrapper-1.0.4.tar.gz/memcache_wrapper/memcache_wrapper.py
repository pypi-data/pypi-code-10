from functools import wraps
import hashlib

class Memcached(object):
    '''
    A class which will cache result of the wrapped function

    This class will check if the result of the function with the given
    parameters is in memcached.
    If yes, get results from memcached, otherwise, execute the method and save
    result in memcached with parameters as key.

    @param  prefix: memcache prefix
    @param  mc_client: memcache client
    @param  ttl: time to live in memcache, default: 10
    @param  bypass_cache: if True, bypass cache and save the result
    @param  cache_negative: if False, do not cache negative result,
                            such as [], {}, and None. Otherwise, it will cache
                            everything.

    Usage:
    @Memcached('/myprefix', mc_client, 60)
    def myfunc(self, var1, var2):
        pass

    or

    mc = Memcached('/myprefix', mc_client)
    cached_myfunc = mc.wrap(myfunc)

    for short,
    cached_myfunc = Memcached('/myprefix', mc_client).wrap(myfunc)
    '''

    def __init__(self, prefix, mc_client=None, ttl=10, bypass_cache=False,
                 cache_negative=False):
        self._prefix = prefix
        self._mc_client = mc_client
        self._ttl = ttl
        self._bypass_cache = bypass_cache
        self._cache_negative = cache_negative

    @staticmethod
    def safe_truncate(key):
        new_key = key[0:216] + hashlib.md5(key).hexdigest()
        # Length of new key: 216 + 32 = 248
        return new_key

    def wrap(self, method):
        return self(method)

    def __call__(self, method):
        @wraps(method)
        def wrapped(*args, **kwargs):
            key = '%s%s%s%s' % (self._prefix, method.__name__,
                                str(args), str(kwargs))
            if len(key) > 250:
                # memcache key length limit: 250
                key = self.safe_truncate(key)
            if self._mc_client and not self._bypass_cache:
                cache = self._mc_client.get(key)
                if cache is not None:
                    return cache

            result = method(*args, **kwargs)
            if self._mc_client and (result or self._cache_negative):
                self._mc_client.set(key, result, self._ttl)
            return result
        return wrapped

