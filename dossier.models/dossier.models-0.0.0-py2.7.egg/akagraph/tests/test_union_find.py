# -*- coding: utf-8 -*-

from __future__ import absolute_import
import pytest
from operator import itemgetter

from dossier.akagraph.core import AKAGraph, soft_selectors

fake_data = [
    {
        u"url": u"a",
        u"name": [u"foo"],
        u"email": [u"foo@mail.com"],
        u"icq": [u"icq1"],
    },{
        u"url": u"b",
        u"name": [u"кс"],
        u"icq": [u"icq1"],
        u"skype": [u"skype1"],
        u"username": [u"username1"],
    },{
        u"url": u"c",
        u"skype": [u"skype1"],
        u"name": [u"x"],
        u"username": [u"username1"],
    },
]

@pytest.yield_fixture(scope='function')
def populated_akagraph():
    client = AKAGraph(['elasticsearch.diffeo.com'],
             'test_akagraph')
    with client:
        map(client.add, fake_data)
    client.sync()
    yield client
    client.delete_index()

@pytest.yield_fixture(scope='function', params=fake_data)
def record(request):
    yield request.param

def test_populated(populated_akagraph, record):
    assert populated_akagraph.get_rec(record['url'])

def test_raise_not_there(populated_akagraph):
    with pytest.raises(KeyError):
        populated_akagraph.get_rec('not-there')

def test_roots(populated_akagraph, record):
    populated_akagraph.root(record['url'])

def test_get_parent(populated_akagraph, record):
    populated_akagraph.get_parent(record['url'])

def test_get_children(populated_akagraph, record):
    populated_akagraph.get_children(record['url'])

def test_connected_component(populated_akagraph):
    assert set('abc') == set(list(populated_akagraph.connected_component('a')))

def test_find_equivs(populated_akagraph, record):
    equivs = set(map(itemgetter(1), populated_akagraph.find_equivs([record])))
    assert len(equivs) > 0
    assert record['url'] not in equivs

#def test_find_perf(populated_akagraph, record):
#    equivs = list(populated_akagraph.find_equivs(record))
#    assert len(equivs) > 0

def test_find_equivs_specific(populated_akagraph):
    # check the a=b U b=c structure of fake_data
    def get_one(i):
        _, equivs = list(populated_akagraph.find_equivs([fake_data[i]]))[0]
        return list(equivs)
    assert fake_data[0]['url'] == 'a'
    assert fake_data[1]['url'] == 'b'
    assert fake_data[2]['url'] == 'c'
    assert ['b'] == get_one(0)
    assert ['b'] == get_one(2)
    assert set(['a', 'c']) == set(get_one(1))

def test_set_parent(populated_akagraph):
    populated_akagraph.set_parent(('u1', 'u2'))
    populated_akagraph.sync()
    assert populated_akagraph.get_parent('u1') == 'u2'

def test_unite(populated_akagraph):
    urls = [rec['url'] for rec in fake_data]
    populated_akagraph.unite(*urls)
    populated_akagraph.sync()
    for u in urls:
        assert populated_akagraph.find(u, urls[0])

def test_find(populated_akagraph, record):
    # verify that ingest actually found and united the three; requires
    # `sync` call in the middle of the two-stage ingest process in
    # `flush` method.
    assert populated_akagraph.find(record['url'], fake_data[0]['url'])

def test_find_equivs_by_selector(populated_akagraph, record):
    for key, values in record.items():
        if key == 'url': continue
        if key in set(soft_selectors): continue
        for val in values:
            equivs = populated_akagraph.find_equivs_by_selector(val)
            equivs = set(list(equivs))
            assert equivs == set(['a']) # finds root the one connected component

def test_find_connected_components(populated_akagraph, record):
    for key, values in record.items():
        if key == 'url': continue
        if key in set(soft_selectors): continue
        for val in values:
            ccs = populated_akagraph.find_connected_components(val)
            ccs = list(ccs)
            assert len(ccs) == 1
            assert set('abc') == set([rec['url'] for rec in ccs[0]])
