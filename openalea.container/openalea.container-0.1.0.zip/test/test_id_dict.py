from copy import deepcopy
from nose.tools import assert_raises

from openalea.container.id_dict import IdDict


def test_id_dict_raise_error_if_key_is_not_int():
    d = IdDict()
    assert_raises(KeyError, lambda: d.__setitem__('a', None))
    assert_raises(KeyError, lambda: d.setdefault('a', None))
    assert_raises(KeyError, lambda: d.add('a', 'key'))


def test_id_dict_behave_like_normal_dict():
    d = IdDict()
    d[10] = None
    assert d[10] is None
    assert d.pop(10) is None
    assert_raises(KeyError, lambda: d.pop(10))
    assert d.pop(10, None) is None
    assert len(d) == 0
    d[1] = 'a'
    d[1] = 'b'
    assert d.popitem() == (1, 'b')
    d[2] = 1
    assert 10 not in d
    assert 2 in d
    assert d.get(10, 'a') == 'a'
    assert d.get(2, None) == 1
    assert len(d) == 1
    assert tuple(d.keys()) == (2,)
    assert tuple(d.values()) == (1,)
    assert tuple(d.items()) == ((2, 1),)

    tmp = {1: 2, 3: 'c'}
    d = IdDict(tmp)
    assert len(d) == 2

    # TODO update not implemented
    # d[1] = 3
    # tmp[5] = 'd'
    # d.update(tmp)
    # assert len(d) == 3
    # assert d[1] == 2

    d.clear()
    assert len(d) == 0

    d = IdDict(tmp)
    del d[1]
    assert 1 not in d

    d.setdefault(10, []).append(10)
    assert 10 in d[10]

    d[23] = [1, 2]
    dd = d.copy()
    assert id(dd) != id(d)
    assert tuple(dd.items()) == tuple(d.items())
    d[23][0] = 10
    assert dd[23][0] == 10

    dd = deepcopy(d)
    assert id(dd) != id(d)
    assert tuple(dd.items()) == tuple(d.items())
    d[23][0] = 100
    assert dd[23][0] != 100


def test_id_dict_only_handle_some_id_gen():
    for gen in ('max', 'set', 'list'):
        IdDict(idgenerator=gen)
    assert_raises(UserWarning, lambda: IdDict(idgenerator='tutu'))


def test_id_dict_generate_id():
    d = IdDict()
    d.add('a')
    assert len(d) == 1
    assert 'a' in d.values()

    d.add('a')
    assert len(d) == 2


def test_id_dict_is_cautious_about_ids():
    tmp = {1: 2, 2: 3}
    d = IdDict(tmp)
    assert len(d) == 2
    d.add('a')
    assert len(d) == 3
    d.add('a')
    assert len(d) == 4


def test_id_dict_refuse_to_reuse_ids():
    d = IdDict()
    d[0] = 'a'
    d.add('b')
    assert len(d) == 2
    assert_raises(KeyError, lambda: d.add('c', 0))
