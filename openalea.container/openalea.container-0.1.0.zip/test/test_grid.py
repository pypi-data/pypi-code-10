from nose.tools import assert_raises

from openalea.container.grid import Grid


def test_grid_can_be_empty():
    g = Grid(())
    assert len(g) == 0
    assert g.dim() == 0
    assert tuple(g.shape()) == ()


def test_grid_can_have_a_single_cell():
    shape = ()
    for i in range(10):
        shape = shape + (1,)
        g = Grid(shape)
        assert len(g) == 1
        assert g.dim() == len(shape)
        assert tuple(g.shape()) == shape


def test_grid_one_dim_same_as_list():
    l = list(range(10))
    g = Grid((len(l),))
    assert len(g) == len(l)
    assert g.dim() == 1
    assert tuple(g) == tuple(l)

    for i in l:
        assert g.coordinates(i) == (i,)
        assert g.index((i,)) == i


def test_grid_coord_start_0_end_len():
    g = Grid((10, 10, 9, 8, 7))
    assert g.index((0, 0, 0, 0, 0)) == 0
    assert g.coordinates(0) == (0, 0, 0, 0, 0)
    assert g.index((9, 9, 8, 7, 6)) == len(g) - 1
    assert g.coordinates(len(g) - 1) == (9, 9, 8, 7, 6)


def test_grid_coord_index_are_inverse():
    g = Grid((1, 2, 3, 4))
    for i in range(len(g)):
        assert g.index(g.coordinates(i)) == i


def test_grid_can_be_null_along_one_axis():
    g = Grid((3, 0, 4))
    assert len(g) == 0
    assert g.dim() == 3
    assert_raises(IndexError, lambda: g.index((0, 0, 0)))
    assert_raises(IndexError, lambda: g.coordinates(0))


def test_grid_raise_error_if_index_out_of_bound():
    g = Grid((10, 9))
    assert_raises(IndexError, lambda: g.coordinates(-1))
    assert_raises(IndexError, lambda: g.coordinates(len(g)))
    assert_raises(IndexError, lambda: g.coordinates(len(g) + 10))


def test_grid_raise_error_if_coord_out_of_bound():
    g = Grid((8, 7))
    assert_raises(IndexError, lambda: g.index((-1, 0)))
    assert_raises(IndexError, lambda: g.index((0, -1)))
    assert_raises(IndexError, lambda: g.index((8, 0)))
    assert_raises(IndexError, lambda: g.index((0, 7)))
    assert_raises(IndexError, lambda: g.index((9, 0)))
    assert_raises(IndexError, lambda: g.index((0, 8)))
