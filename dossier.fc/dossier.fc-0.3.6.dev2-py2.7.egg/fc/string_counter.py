'''dossier.fc Feature Collections

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.

.. autoclass:: StringCounter
'''
from __future__ import absolute_import, division, print_function
try:
    from collections import Counter
except ImportError:
    from backport_collections import Counter
from collections import Mapping, MutableMapping
from functools import wraps

from dossier.fc.exceptions import ReadOnlyException, uni


def mutates(f):
    '''Decorator for functions that mutate :class:`StringCounter`.

    This raises :exc:`~dossier.fc.exceptions.ReadOnlyException` if
    the object is read-only, and increments the generation counter
    otherwise.
    '''
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.read_only:
            raise ReadOnlyException()
        self.next_generation()
        return f(self, *args, **kwargs)
    return wrapper


class StringCounter(Counter):
    '''Simple counter based on exact string matching.

    This is a subclass of :class:`collections.Counter` that includes a
    generation counter so that it can be used in a cache.

    :class:`StringCounter` is the default feature type in a feature
    collection, so you typically don't have to instantiate a
    :class:`StringCounter` explicitly::

        fc = FeatureCollection()
        fc['NAME']['John Smith'] += 1

    But instantiating directly works too::

        sc = StringCounter()
        sc['John Smith'] += 1

        fc = FeatureCollection({'NAME': sc})
        fc['NAME']['John Smith'] += 1
        assert fc['NAME']['John Smith'] == 2

    Note that instances of this class support all the methods defined
    for a :class:`collections.Counter`, but only the ones unique to
    :class:`StringCounter` are listed here.

    .. automethod:: __init__
    .. automethod:: truncate_most_common

    .. attribute:: read_only

        Flag indicating whether this collection is read-only.

        This flag always begins as :const:`False`, it cannot be set
        via the constructor for compatibility with
        :class:`collections.Counter`.  If this flag is set, then any
        operations that mutate it will raise
        :exc:`~dossier.fc.exceptions.ReadOnlyException`.

    .. attribute:: generation

        Generation number for this counter instance.

        This number is incremented by every operation that
        mutates the counter object.  If two collections are the
        same object and have the same generation number, then
        they are identical.

        Having this property allows a pair of `id(sc)` and the
        generation to be an immutable hashable key for things like
        memoization operations, accounting for the possibility of the
        counter changing over time.

        >>> sc = StringCounter({'a': 1})
        >>> cache = {(id(sc), sc.generation): 1}
        >>> (id(sc), sc.generation) in cache
        True
        >>> sc['a']
        1
        >>> (id(sc), sc.generation) in cache
        True
        >>> sc['a'] += 1
        >>> sc['a']
        2
        >>> (id(sc), sc.generation) in cache
        False

    '''

    current_generation = 0
    '''Class-static generation number.

    Each mutation of a StringCounter increments this generation,
    and sets the counter's current generation to this value.
    See :meth:`next_generation` for details.
    '''

    def __init__(self, *args, **kwargs):
        '''Initialize a :class:`StringCounter` with existing counts::

            >>> sc = StringCounter(a=4, b=2, c=0)
            >>> sc['b']
            2

        See the documentation for :class:`collections.Counter` for more
        examples.
        '''

        self.read_only = False
        self.generation = self.current_generation
        super(StringCounter, self).__init__(*args, **kwargs)

    def next_generation(self):
        '''Increment the generation counter on this collection.'''
        self.current_generation += 1
        self.generation = self.current_generation

    @mutates
    def __delitem__(self, key):
        return super(StringCounter, self).__delitem__(key)

    @staticmethod
    def _fix_key(key):
        '''Normalize keys to Unicode strings.'''
        if isinstance(key, unicode):
            return key
        if isinstance(key, str):
            # On my system, the default encoding is `ascii`, so let's
            # explicitly say UTF-8?
            return unicode(key, 'utf-8')
        raise TypeError(key)

    @mutates
    def __setitem__(self, key, value):
        key = self._fix_key(key)
        return super(StringCounter, self).__setitem__(key, value)

    @mutates
    def pop(self, key):
        return super(StringCounter, self).pop(key)

    @mutates
    def popitem(self, key):
        return super(StringCounter, self).popitem(key)

    @mutates
    def subtract(self, other):
        return super(StringCounter, self).subtract(other)

    @mutates
    def update(self, iterable=None, **kwargs):
        # Force all keys into Unicode strings before calling base
        # class implementation; if kwargs is non-empty then the base
        # class will call this method again
        if iterable:
            if isinstance(iterable, Mapping):
                new_iterable = {}
                for (k, v) in iterable.iteritems():
                    new_iterable[self._fix_key(k)] = v
                iterable = new_iterable
            else:
                iterable = (self._fix_key(k) for k in iterable)
        return super(StringCounter, self).update(iterable, **kwargs)

    def __add__(self, other):
        result = super(StringCounter, self).__add__(other)
        return StringCounter(result)

    def __sub__(self, other):
        result = super(StringCounter, self).__sub__(other)
        return StringCounter(result)

    @mutates
    def __imul__(self, coef):
        for k in self.keys():
            self[k] *= coef
        return self

    @mutates
    def truncate_most_common(self, truncation_length):
        '''
        Sorts the counter and keeps only the most common items up to
        ``truncation_length`` in place.

        :type truncation_length: int
        '''
        keep_keys = set(v[0] for v in self.most_common(truncation_length))
        for key in self.keys():
            if key not in keep_keys:
                self.pop(key)


class StringCounterSerializer(object):
    def __init__(self):
        raise NotImplementedError()

    loads = StringCounter

    @staticmethod
    def dumps(sc):
        return dict(sc)

    constructor = StringCounter


class NestedStringCounter(MutableMapping):
    '''A mapping from string to string counter.
    '''
    def __init__(self, data=None):
        self.data = {}
        if data is not None:
            for fname, counter in data.items():
                if fname not in self.data:
                    self.data[fname] = StringCounter()
                for key, count in counter.iteritems():
                    self.data[fname][key] = count

    def to_nested_dict(self):
        dumped = {}
        for key, counter in self.data.iteritems():
            dumped[key] = dict(counter)
        return dumped

    @staticmethod
    def from_nested_dict(d):
        return NestedStringCounter(data=d)

    def __getitem__(self, key):
        return self.data.get(uni(key)) or self.__missing__(key)

    def __missing__(self, key):
        v = StringCounter()
        self[uni(key)] = v
        return v

    def __contains__(self, key):
        return key in self.data

    def __setitem__(self, key, value):
        self.data[uni(key)] = value

    def __delitem__(self, key):
        del self.data[uni(key)]

    def __len__(self): return len(self.data)

    def __iter__(self): return iter(self.data)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.data))

    def __add__(self, other):
        new_nsc = NestedStringCounter(self.to_nested_dict())
        for key, counter in other.items():
            if key in new_nsc:
                new_nsc[key] += counter
            else:
                new_nsc[key] = counter
        return new_nsc

class NestedStringCounterSerializer(object):
    '''Serialize nested string counters.'''

    def __init__(self):
        raise NotImplementedError()

    dumps = NestedStringCounter.to_nested_dict
    constructor = NestedStringCounter

    @staticmethod
    def loads(d):
        return NestedStringCounter.from_nested_dict(d)
