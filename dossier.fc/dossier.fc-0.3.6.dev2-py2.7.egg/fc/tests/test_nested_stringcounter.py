'''tests for NestedStringCounter

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.

'''

from dossier.fc import FeatureCollection
from dossier.fc.string_counter import NestedStringCounter, StringCounter, \
    NestedStringCounterSerializer

def test_nested_fcdefault():
    fc = FeatureCollection()
    assert isinstance(fc['%names'], NestedStringCounter)

def test_nsc_roundtrip():
    fc = FeatureCollection()
    fc['#testing'] = NestedStringCounter()
    fc['#testing']['foo'] = StringCounter({'foo': 1})
    fc['#testing']['bar'] = StringCounter({'foo': 2, 'bar': 1})
    dumped = fc.dumps()
    assert FeatureCollection.loads(dumped) == fc

def test_nsc():
    data = {'foo': StringCounter({'bar': 1}),
            'baz': StringCounter({'bar': 1})}

    nsc = NestedStringCounter(data=data)
    out = NestedStringCounterSerializer.dumps(nsc)
    nsc2 = NestedStringCounterSerializer.loads(out)

    assert nsc2 is not nsc
    assert nsc2 == nsc

def test_nsc_add():
    data1 = {'foo': StringCounter({'bar': 1}),
             'baz': StringCounter({'bar': 1})}
    data2 = {'foo': StringCounter({'foo': 1, 'bar': 2}),
             'bar': StringCounter({'baz': 1})}

    nsc1 = NestedStringCounter(data=data1)
    nsc2 = NestedStringCounter(data=data2)

    # Sum of two counters.
    added = nsc1 + nsc2
    assert added['foo'] == StringCounter({'bar': 3, 'foo': 1})
    assert added['baz'] == StringCounter({'bar': 1})
    assert added['bar'] == StringCounter({'baz': 1})

    # Original counters unchanged.
    assert nsc1['foo'] == StringCounter({'bar': 1})
    assert nsc1['baz'] == StringCounter({'bar': 1})
    assert 'bar' not in nsc1

    assert nsc2['foo'] == StringCounter({'foo': 1, 'bar': 2})
    assert nsc2['bar'] == StringCounter({'baz': 1})
    assert 'baz' not in nsc2

    # Test in-place.
    nsc1 += nsc2
    assert nsc1 == added
