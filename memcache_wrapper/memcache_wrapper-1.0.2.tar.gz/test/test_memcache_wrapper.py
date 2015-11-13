import unittest
import time

from mockito import mock
from mockcache import Client
from memcache_wrapper import Memcached

mc_client = Client()


class TestMemcached(unittest.TestCase):
    def test_cache_hit(self):
        functions = [self.decorate_myfunc]

        for f in functions:
            v1 = f(1)
            v2 = f(1)
            assert v1 == v2

    def test_cache_miss(self):
        functions = [self.decorate_myfunc]

        for f in functions:
            v1 = f(1)
            v2 = f(2)
            assert v1 != v2

    def test_no_mc_client(self):
        wrapper = Memcached('/myprefix')
        myfunc = wrapper.wrap(self.myfunc)
        functions = [myfunc]

        for f in functions:
            v1 = f(1)
            v2 = f(1)
            v3 = f(1)
            assert v1 != v2
            assert v2 != v3

    def test_negative(self):
        mc_client = mock()

        def dummy(a, b, c):
            raise Exception('negative result should not be saved')

        mc_client.set = dummy
        wrapper = Memcached('/myprefix', mc_client, cache_negative=False)
        myfunc = wrapper.wrap(self.negative)

        functions = [self.decorate_negative, myfunc]
        for f in functions:
            v1 = f(1)
            v2 = f(1)
            assert v1 == v2

    def test_cache_bypass(self):
        wrapper = Memcached('/myprefix', mc_client, bypass_cache=True)
        myfunc = wrapper.wrap(self.myfunc)
        v1 = myfunc(1)
        v2 = myfunc(1)
        assert v1 != v2

        # check v2 is saved
        wrapper = Memcached('/myprefix', mc_client)
        mynewfunc = wrapper.wrap(self.myfunc)
        v3 = mynewfunc(1)
        assert v2 == v3

    def test_cache_safe_truncate(self):
        key1 = 'a' * 4096
        key2 = 'a' * 4096 + 'b'
        new_key1 = Memcached.safe_truncate(key1)
        new_key2 = Memcached.safe_truncate(key2)
        assert len(new_key1) < 250
        assert len(new_key2) < 250
        assert new_key1 != new_key2

    @Memcached('/myprefix', mc_client)
    def decorate_myfunc(self, t):
        return time.time()

    @Memcached('/myprefix', mc_client, cache_negative=False)
    def decorate_negative(self, t):
        return {}

    def myfunc(self, t):
        return time.time()

    def negative(self, t):
        return {}
