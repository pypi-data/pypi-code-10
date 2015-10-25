from __future__ import absolute_import, division, print_function

from operator import add
from copy import deepcopy

import dask
import pytest

from dask.async import *


fib_dask = {'f0': 0, 'f1': 1, 'f2': 1, 'f3': 2, 'f4': 3, 'f5': 5, 'f6': 8}


def test_start_state():
    dsk = {'x': 1, 'y': 2, 'z': (inc, 'x'), 'w': (add, 'z', 'y')}
    result = start_state_from_dask(dsk)

    expeted = {'cache': {'x': 1, 'y': 2},
               'dependencies': {'w': set(['y', 'z']),
                                'x': set([]),
                                'y': set([]),
                                'z': set(['x'])},
               'dependents': {'w': set([]),
                              'x': set(['z']),
                              'y': set(['w']),
                              'z': set(['w'])},
               'finished': set([]),
               'released': set([]),
               'running': set([]),
               'ready': ['z'],
               'waiting': {'w': set(['z'])},
               'waiting_data': {'x': set(['z']),
                                'y': set(['w']),
                                'z': set(['w'])}}

def test_start_state_looks_at_cache():
    dsk = {'b': (inc, 'a')}
    cache = {'a': 1}
    result = start_state_from_dask(dsk, cache)
    assert result['dependencies']['b'] == set(['a'])
    assert result['ready'] == ['b']


def test_start_state_with_redirects():
    dsk = {'x': 1, 'y': 'x', 'z': (inc, 'y')}
    result = start_state_from_dask(dsk)
    assert result['cache'] == {'x': 1}


def test_start_state_with_independent_but_runnable_tasks():
    assert start_state_from_dask({'x': (inc, 1)})['ready'] == ['x']


def test_finish_task():
    dsk = {'x': 1, 'y': 2, 'z': (inc, 'x'), 'w': (add, 'z', 'y')}
    sortkey = order(dsk).get
    state = start_state_from_dask(dsk)
    state['ready'].remove('z')
    state['running'] = set(['z', 'other-task'])
    task = 'z'
    result = 2

    oldstate = deepcopy(state)
    state['cache']['z'] = result
    finish_task(dsk, task, state, set(), sortkey)

    assert state == {
          'cache': {'y': 2, 'z': 2},
          'dependencies': {'w': set(['y', 'z']),
                           'x': set([]),
                           'y': set([]),
                           'z': set(['x'])},
          'finished': set(['z']),
          'released': set(['x']),
          'running': set(['other-task']),
          'dependents': {'w': set([]),
                         'x': set(['z']),
                         'y': set(['w']),
                         'z': set(['w'])},
          'ready': ['w'],
          'waiting': {},
          'waiting_data': {'y': set(['w']),
                           'z': set(['w'])}}


def test_get():
    dsk = {'x': 1, 'y': 2, 'z': (inc, 'x'), 'w': (add, 'z', 'y')}
    assert get_sync(dsk, 'w') == 4
    assert get_sync(dsk, ['w', 'z']) == (4, 2)


def test_nested_get():
    dsk = {'x': 1, 'y': 2, 'a': (add, 'x', 'y'), 'b': (sum, ['x', 'y'])}
    assert get_sync(dsk, ['a', 'b']) == (3, 3)


def test_cache_options():
    try:
        from chest import Chest
    except ImportError:
        return
    cache = Chest()
    def inc2(x):
        assert 'y' in cache
        return x + 1

    with dask.set_options(cache=cache):
        get_sync({'x': (inc2, 'y'), 'y': 1}, 'x')


def test_sort_key():
    L = ['x', ('x', 1), ('z', 0), ('x', 0)]
    assert sorted(L, key=sortkey) == ['x', ('x', 0), ('x', 1), ('z', 0)]


def test_callback():
    f = lambda x: x + 1
    dsk = {'a': (f, 1)}
    from dask.threaded import get

    def start_callback(key, d, state):
        assert key == 'a' or key is None
        assert d == dsk
        assert isinstance(state, dict)

    def end_callback(key, value, d, state, worker_id):
        assert key == 'a' or key is None
        assert value == 2 or value is None
        assert d == dsk
        assert isinstance(state, dict)

    get(dsk, 'a', start_callback=start_callback, end_callback=end_callback)


def test_order_of_startstate():
    dsk = {'a': 1, 'b': (inc, 'a'), 'c': (inc, 'b'),
           'x': 1, 'y': (inc, 'x')}
    result = start_state_from_dask(dsk)

    assert result['ready'] == ['y', 'b']

    dsk = {'x': 1, 'y': (inc, 'x'), 'z': (inc, 'y'),
           'a': 1, 'b': (inc, 'a')}
    result = start_state_from_dask(dsk)

    assert result['ready'] == ['b', 'y']


def test_nonstandard_exceptions_propagate():
    class MyException(Exception):
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def __str__(self):
            return "My Exception!"

    def f():
        raise MyException(1, 2)

    from dask.threaded import get

    try:
        get({'x': (f,)}, 'x')
        assert False
    except MyException as e:
        assert "My Exception!" in str(e)
        assert "Traceback" in str(e)
        assert 'a' in dir(e)
        assert 'traceback' in dir(e)
        assert e.exception.a == 1 and e.exception.b == 2
        assert e.a == 1 and e.b == 2


def test_remote_exception():
    e = TypeError("hello")
    a = remote_exception(e, 'traceback')
    b = remote_exception(e, 'traceback')

    assert type(a) == type(b)
    assert isinstance(a, TypeError)
    assert 'hello' in str(a)
    assert 'traceback' in str(a)
