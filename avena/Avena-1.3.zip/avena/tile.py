#!/usr/bin/env python

"""Tiling of image arrays."""


import numpy

from . import flip, image, np


def _num_tiles(array, tile_shape):
    m, n = array.shape
    a, b = tile_shape
    p = int(numpy.ceil(float(m) / a))
    q = int(numpy.ceil(float(n) / b))
    return (p, q)


def _tile_at(array, tile_shape, indices):
    a, b = tile_shape
    i, j = indices
    return array[(i * a):(i * a + a), (j * b):(j * b + b)]


def _map_to_tiles(func, shape_func, tile_shape, array):
    m, n = _num_tiles(array, tile_shape)
    a, b = tile_shape
    c, d = shape_func(tile_shape)
    e, f = shape_func(array.shape)
    array = np._zeropad(array, (m * a, n * b))
    result = numpy.zeros((m * c, n * d), dtype=array.dtype)
    indices = ((i, j) for i in range(m) for j in range(n))
    for (i, j) in indices:
        x = _tile_at(array, (a, b), (i, j))
        z = _tile_at(result, (c, d), (i, j))
        z[:, :] = func(x)
    return result[:e, :f]


def _tile9_periodic_shape(shape):
    m, n = shape
    return (3 * m, 3 * n)


def _tile9_periodic(array):
    m, n = array.shape
    z = numpy.zeros(_tile9_periodic_shape((m, n)), dtype=array.dtype)
    xfv = flip._flip_vertical(array)
    xfh = flip._flip_horizontal(array)
    xfb = flip._flip_horizontal(flip._flip_vertical(array))
    tile0 = z[m:(2 * m), n:(2 * n)]
    tile1 = z[:m, n:(2 * n)]
    tile2 = z[:m, (2 * n):(3 * n)]
    tile3 = z[m:(2 * m), (2 * n):(3 * n)]
    tile4 = z[(2 * m):(3 * m), (2 * n):(3 * n)]
    tile5 = z[(2 * m):(3 * m), n:(2 * n)]
    tile6 = z[(2 * m):(3 * m), :n]
    tile7 = z[m:(2 * m), :n]
    tile8 = z[:m, :n]
    tile0[:, :] = array[:, :]
    tile1[:, :] = xfv[:, :]
    tile2[:, :] = xfb[:, :]
    tile3[:, :] = xfh[:, :]
    tile4[:, :] = xfb[:, :]
    tile5[:, :] = xfv[:, :]
    tile6[:, :] = xfb[:, :]
    tile7[:, :] = xfh[:, :]
    tile8[:, :] = xfb[:, :]
    return z


def tile9_periodic(img):
    """Tile an image into a 3x3 periodic grid."""
    return image.map_to_channels(
        _tile9_periodic,
        _tile9_periodic_shape,
        img,
    )


if __name__ == '__main__':
    pass
