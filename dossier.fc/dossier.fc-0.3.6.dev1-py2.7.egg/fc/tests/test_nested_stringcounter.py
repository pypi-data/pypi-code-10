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
