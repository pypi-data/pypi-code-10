import unittest

import cachetools


class DecoratorTestMixin(object):

    def cache(self, minsize):
        raise NotImplementedError

    def func(self, *args, **kwargs):
        if hasattr(self, 'count'):
            self.count += 1
        else:
            self.count = 0
        return self.count

    def test_decorator(self):
        cache = self.cache(2)
        wrapper = cachetools.cached(cache)(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)

        self.assertEqual(wrapper(0), 0)
        self.assertEqual(len(cache), 1)
        self.assertIn(cachetools.hashkey(0), cache)
        self.assertNotIn(cachetools.hashkey(1), cache)
        self.assertNotIn(cachetools.hashkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)
        self.assertIn(cachetools.hashkey(0), cache)
        self.assertIn(cachetools.hashkey(1), cache)
        self.assertIn(cachetools.hashkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual(wrapper(1.0), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual(wrapper(1.0), 1)
        self.assertEqual(len(cache), 2)

    def test_decorator_typed(self):
        cache = self.cache(3)

        def typedkey(*args, **kwargs):
            key = cachetools.hashkey(*args, **kwargs)
            key += tuple(type(v) for v in args)
            key += tuple(type(v) for _, v in sorted(kwargs.items()))
            return key
        wrapper = cachetools.cached(cache, key=typedkey)(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)

        self.assertEqual(wrapper(0), 0)
        self.assertEqual(len(cache), 1)
        self.assertIn(typedkey(0), cache)
        self.assertNotIn(typedkey(1), cache)
        self.assertNotIn(typedkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)
        self.assertIn(typedkey(0), cache)
        self.assertIn(typedkey(1), cache)
        self.assertNotIn(typedkey(1.0), cache)

        self.assertEqual(wrapper(1), 1)
        self.assertEqual(len(cache), 2)

        self.assertEqual(wrapper(1.0), 2)
        self.assertEqual(len(cache), 3)
        self.assertIn(typedkey(0), cache)
        self.assertIn(typedkey(1), cache)
        self.assertIn(typedkey(1.0), cache)

        self.assertEqual(wrapper(1.0), 2)
        self.assertEqual(len(cache), 3)

    def test_decorator_lock(self):
        class Lock(object):

            count = 0

            def __enter__(self):
                Lock.count += 1

            def __exit__(self, *exc):
                pass

        cache = self.cache(2)
        wrapper = cachetools.cached(cache, lock=Lock())(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)
        self.assertEqual(wrapper(0), 0)
        self.assertEqual(Lock.count, 2)
        self.assertEqual(wrapper(1), 1)
        self.assertEqual(Lock.count, 4)
        self.assertEqual(wrapper(1), 1)
        self.assertEqual(Lock.count, 5)


class CacheWrapperTest(unittest.TestCase, DecoratorTestMixin):

    def cache(self, minsize):
        return cachetools.Cache(maxsize=minsize)

    def test_zero_size_cache_decorator(self):
        cache = self.cache(0)
        wrapper = cachetools.cached(cache)(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)

        self.assertEqual(wrapper(0), 0)
        self.assertEqual(len(cache), 0)

    def test_zero_size_cache_decorator_lock(self):
        class Lock(object):

            count = 0

            def __enter__(self):
                Lock.count += 1

            def __exit__(self, *exc):
                pass

        cache = self.cache(0)
        wrapper = cachetools.cached(cache, lock=Lock())(self.func)

        self.assertEqual(len(cache), 0)
        self.assertEqual(wrapper.__wrapped__, self.func)

        self.assertEqual(wrapper(0), 0)
        self.assertEqual(len(cache), 0)
        self.assertEqual(Lock.count, 2)


class DictWrapperTest(unittest.TestCase, DecoratorTestMixin):

    def cache(self, minsize):
        return dict()


class NoneWrapperTest(unittest.TestCase):

    def func(self, *args, **kwargs):
        return args + tuple(kwargs.items())

    def test_decorator(self):
        wrapper = cachetools.cached(None)(self.func)
        self.assertEqual(wrapper.__wrapped__, self.func)

        self.assertEqual(wrapper(0), (0,))
        self.assertEqual(wrapper(1), (1,))
        self.assertEqual(wrapper(1, foo='bar'), (1, ('foo', 'bar')))
