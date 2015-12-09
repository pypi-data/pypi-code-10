def test_property_access():
    from telemetronclient.utils.map import Map

    map_ = Map({'foo': "this is foo", 'bar': "This is bar!"})
    assert hasattr(map_, 'foo')
    assert hasattr(map_, 'bar')

def test_expect_kwargs_to_be_used():
    from telemetronclient.utils.map import Map

    map_ = Map({'foo': "this is foo"}, bar="This is bar!")
    assert hasattr(map_, 'foo')
    assert hasattr(map_, 'bar')

def test_expect_del_to_remove_element():
    from telemetronclient.utils.map import Map

    map_ = Map({'foo': "this is foo"}, bar="This is bar!")
    del map_.foo
    assert 'foo' not in map_
