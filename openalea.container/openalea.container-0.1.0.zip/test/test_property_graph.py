from nose.tools import assert_raises, with_setup
from openalea.container.graph import Graph
from openalea.container.property_graph import (PropertyGraph,
                                               InvalidVertex,
                                               InvalidEdge,
                                               InvalidProperty)


g = PropertyGraph()
g.add_vertex_property("prop")
g.add_edge_property("prop")


def setup_func():
    for i in range(10):
        g.add_vertex(i)
        g.vertex_property("prop")[i] = 'v%d' % i
    for i in range(9):
        g.add_edge(i, i + 1, i)
        g.edge_property("prop")[i] = 'e%d' % i


def teardown_func():
    g.clear()


@with_setup(setup_func, teardown_func)
def test_pg_has_no_property_by_default():
    pg = PropertyGraph()
    assert len(tuple(pg.vertex_property_names())) == 0
    assert len(tuple(pg.edge_property_names())) == 0
    assert len(tuple(pg.graph_property_names())) == 0
    assert len(tuple(pg.vertex_properties())) == 0
    assert len(tuple(pg.edge_properties())) == 0
    assert len(tuple(pg.graph_properties())) == 0


@with_setup(setup_func, teardown_func)
def test_pg_prop_is_empty_on_creation_by_default():
    g.add_vertex_property("new_prop")
    assert "new_prop" in g.vertex_property_names()
    assert len(g.vertex_property("new_prop")) == 0

    g.add_edge_property("new_prop")
    assert "new_prop" in g.edge_property_names()
    assert len(g.edge_property("new_prop")) == 0

    g.add_graph_property("prop")
    assert "prop" in g.graph_property_names()
    assert g.graph_property("prop") is None

    g.remove_vertex_property("new_prop")
    g.remove_edge_property("new_prop")
    g.remove_graph_property("prop")


@with_setup(setup_func, teardown_func)
def test_pg_prop_is_not_set_with_new_element():
    vid = g.add_vertex()
    assert vid not in g.vertex_property("prop")

    eid = g.add_edge(0, 2)
    assert eid not in g.edge_property("prop")


@with_setup(setup_func, teardown_func)
def test_pg_prop_is_del_when_removing_an_element():
    vid = 1
    eids = tuple(g.edges(vid))
    assert vid in g.vertex_property("prop")
    for eid in eids:
        assert eid in g.edge_property("prop")
    g.remove_vertex(vid)
    assert vid not in g.vertex_property("prop")
    for eid in eids:
        assert eid not in g.edge_property("prop")

    eid = 7
    sid = g.source(eid)
    tid = g.target(eid)
    assert eid in g.edge_property("prop")
    assert sid in g.vertex_property("prop")
    assert tid in g.vertex_property("prop")
    g.remove_edge(eid)
    assert eid not in g.edge_property("prop")
    assert sid in g.vertex_property("prop")
    assert tid in g.vertex_property("prop")


@with_setup(setup_func, teardown_func)
def test_pg_raise_error_is_access_to_invalid_prop():
    assert_raises(InvalidProperty, lambda: g.vertex_property("toto"))
    assert_raises(InvalidProperty, lambda: g.edge_property("toto"))
    assert_raises(InvalidProperty, lambda: g.graph_property("toto"))


@with_setup(setup_func, teardown_func)
def test_pg_raise_error_if_add_same_prop_twice():
    assert_raises(InvalidProperty, lambda: g.add_vertex_property("prop"))
    assert_raises(InvalidProperty, lambda: g.add_edge_property("prop"))
    g.add_graph_property("prop")
    assert_raises(InvalidProperty, lambda: g.add_graph_property("prop"))


@with_setup(setup_func, teardown_func)
def test_pg_raise_error_is_remove_non_existing_prop():
    assert_raises(InvalidProperty, lambda: g.remove_vertex_property("toto"))
    assert_raises(InvalidProperty, lambda: g.remove_edge_property("toto"))
    assert_raises(InvalidProperty, lambda: g.remove_graph_property("toto"))


@with_setup(setup_func, teardown_func)
def test_pg_clear_keep_property_names():
    pvid = id(g.vertex_property("prop"))
    peid = id(g.edge_property("prop"))
    g.clear()
    assert "prop" in g.vertex_property_names()
    assert "prop" in g.edge_property_names()
    assert len(g.vertex_property("prop")) == 0
    assert len(g.edge_property("prop")) == 0
    assert id(g.vertex_property("prop")) == pvid
    assert id(g.edge_property("prop")) == peid
    assert len(tuple(g.graph_properties())) == 0


@with_setup(setup_func, teardown_func)
def test_pg_clear_edges_keep_property_names():
    pv_len = len(g.vertex_property("prop"))
    peid = id(g.edge_property("prop"))
    g.clear_edges()
    assert "prop" in g.vertex_property_names()
    assert "prop" in g.edge_property_names()
    assert len(g.vertex_property("prop")) == pv_len
    assert len(g.edge_property("prop")) == 0
    assert id(g.edge_property("prop")) == peid


@with_setup(setup_func, teardown_func)
def test_pg_vertex_and_edge_properties_are_not_the_same():
    g.add_vertex_property("toto")
    g.add_edge_property("toto")
    g.vertex_property("toto")[0] = 'a'
    assert 0 not in g.edge_property("toto")


@with_setup(setup_func, teardown_func)
def test_pg_can_be_extended_with_normal_graph():
    sg = Graph()
    for i in range(10):
        sg.add_vertex(i)
    for i in range(9):
        sg.add_edge(i, i + 1, i)

    old_len = len(g)
    old_nb_vprop = len(tuple(g.vertex_property_names()))
    old_nb_eprop = len(tuple(g.edge_property_names()))
    old_nb_gprop = len(tuple(g.graph_property_names()))
    old_len_vprop = len(g.vertex_property("prop"))
    old_len_eprop = len(g.edge_property("prop"))
    g.extend(sg)
    assert len(g) == old_len + len(sg)
    assert len(tuple(g.vertex_property_names())) == old_nb_vprop
    assert len(tuple(g.edge_property_names())) == old_nb_eprop
    assert len(tuple(g.graph_property_names())) == old_nb_gprop
    assert len(g.vertex_property("prop")) == old_len_vprop
    assert len(g.edge_property("prop")) == old_len_eprop


@with_setup(setup_func, teardown_func)
def test_pg_can_be_extended_with_another_graph_with_same_properties():
    old_len = len(g)
    old_nb_vprop = len(tuple(g.vertex_property_names()))
    old_nb_eprop = len(tuple(g.edge_property_names()))
    old_nb_gprop = len(tuple(g.graph_property_names()))
    old_len_vprop = len(g.vertex_property("prop"))
    old_len_eprop = len(g.edge_property("prop"))
    g.extend(g)
    assert len(g) == old_len * 2
    assert len(tuple(g.vertex_property_names())) == old_nb_vprop
    assert len(tuple(g.edge_property_names())) == old_nb_eprop
    assert len(tuple(g.graph_property_names())) == old_nb_gprop
    assert len(g.vertex_property("prop")) == old_len_vprop * 2
    assert len(g.edge_property("prop")) == old_len_eprop * 2


@with_setup(setup_func, teardown_func)
def test_pg_can_be_extended_with_another_graph_with_different_properties():
    pg = PropertyGraph()
    for i in range(5):
        pg.add_vertex(i)
    for i in range(4):
        pg.add_edge(i, i + 1, i)
    pg.add_vertex_property("aprop")
    for vid in pg.vertices():
        pg.vertex_property("aprop")[vid] = 1
    pg.add_edge_property("aprop")
    for eid in pg.edges():
        pg.edge_property("aprop")[eid] = 2
    pg.add_graph_property("gprop", 'a')

    old_len = len(g)
    old_len_vprop = len(g.vertex_property("prop"))
    old_len_eprop = len(g.edge_property("prop"))
    g.extend(pg)
    assert len(g) == old_len + len(pg)
    assert "prop" in g.vertex_property_names()
    assert "aprop" in g.vertex_property_names()
    assert "prop" in g.edge_property_names()
    assert "aprop" in g.edge_property_names()
    assert "gprop" in g.graph_property_names()
    assert len(g.vertex_property("prop")) == old_len_vprop
    assert len(g.edge_property("prop")) == old_len_eprop
    assert len(g.vertex_property("aprop")) == len(pg.vertex_property("aprop"))
    assert len(g.edge_property("aprop")) == len(pg.edge_property("aprop"))
