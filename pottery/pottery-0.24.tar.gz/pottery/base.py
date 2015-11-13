#-----------------------------------------------------------------------------#
#   base.py                                                                   #
#                                                                             #
#   Copyright (c) 2015, Rajiv Bakulesh Shah.                                  #
#   All rights reserved.                                                      #
#-----------------------------------------------------------------------------#



import abc
import contextlib
import functools
import json
import os
import random
import string
import threading

from redis import Redis
from redis import WatchError

from . import monkey
from .exceptions import RandomKeyError
from .exceptions import TooManyTriesError



class Common:
    _DEFAULT_REDIS_URL = 'http://localhost:6379/'
    _NUM_TRIES = 3
    _RANDOM_KEY_PREFIX = 'pottery-'
    _RANDOM_KEY_LENGTH = 16

    @staticmethod
    def _encode(value):
        encoded = json.dumps(value)
        return encoded

    @staticmethod
    def _decode(value):
        decoded = json.loads(value.decode('utf-8'))
        return decoded

    @classmethod
    def _default_redis(cls):
        url = os.environ.get('REDIS_URL', cls._DEFAULT_REDIS_URL)
        redis = Redis.from_url(url)
        return redis

    def __init__(self, *args, redis=None, key=None, **kwargs):
        self.redis = redis
        self.key = key

    def __del__(self):
        if self.key.startswith(self._RANDOM_KEY_PREFIX):
            self.redis.delete(self.key)

    def __eq__(self, other):
        if type(self) == type(other) and self.redis == other.redis and \
           self.key == other.key:
            return True
        equals = super().__eq__(other)
        return equals

    def __ne__(self, other):
        does_not_equal = not self.__eq__(other)
        return does_not_equal

    @property
    def redis(self):
        return self._redis

    @redis.setter
    def redis(self, value):
        self._redis = self._default_redis() if value is None else value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = self._random_key() if value is None else value

    def _random_key(self, *, tries=_NUM_TRIES):
        if tries <= 0:
            raise RandomKeyError(self.redis, self.key)
        all_chars = string.digits + string.ascii_letters
        random_char = functools.partial(random.choice, all_chars)
        suffix = ''.join(random_char() for n in range(self._RANDOM_KEY_LENGTH))
        random_key = self._RANDOM_KEY_PREFIX + suffix
        if self.redis.exists(random_key):
            random_key = self._random_key(tries=tries-1)
        return random_key



class Lockable:
    _lock = threading.Lock()
    _count = {}
    _locks = {}

    def __init__(self, *args, redis=None, key=None, **kwargs):
        super().__init__(*args, redis=redis, key=key, **kwargs)
        with self._lock:
            self._count[self._id] = self._count.get(self._id, 0) + 1
            if self._count[self._id] == 1:
                self._locks[self._id] = threading.Lock()

    def __del__(self):
        super().__del__()
        with self._lock:
            if self._count.get(self._id) is not None:
                self._count[self._id] -= 1
                if self._count[self._id] == 0:
                    del self._count[self._id]
                    del self._locks[self._id]

    @property
    def _id(self):
        instance_id = (self.redis, self.key)
        return instance_id

    @property
    def lock(self):
        instance_lock = self._locks[self._id]
        return instance_lock



class Pipelined:
    @classmethod
    def _watch(cls):
        def wrap1(func):
            @functools.wraps(func)
            def wrap2(self, *args, **kwargs):
                for _ in range(super()._NUM_TRIES):
                    try:
                        original_redis = self.redis
                        self.redis = self.redis.pipeline()
                        self.redis.watch(self.key)
                        value = func(self, *args, **kwargs)
                        self.redis.execute()
                        return value
                    except WatchError:
                        pass
                    finally:
                        self.redis = original_redis
                else:
                    raise TooManyTriesError(self.redis, self.key)
            return wrap2
        return wrap1

    @contextlib.contextmanager
    def _pipeline(self):
        pipeline = self.redis.pipeline()
        try:
            yield pipeline
        finally:
            pipeline.execute()



class Clearable:
    def clear(self):
        'Remove the elements in a Redis-backed container.  O(n)'
        self.redis.delete(self.key)



class ContextManaged:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
        self._redis.connection_pool.disconnect()



class Base(ContextManaged, Clearable, Pipelined, Lockable, Common):
    ...



class Iterable(metaclass=abc.ABCMeta):
    def __iter__(self):
        'Iterate over the items in a Redis-backed container.  O(n)'
        cursor = 0
        while True:
            cursor, iterable = self._scan(self.key, cursor=cursor)
            for value in iterable:
                decoded = self._decode(value)
                yield decoded
            if cursor == 0:
                break

    @abc.abstractmethod
    def _scan(self, key, *, cursor=0):
        ...
