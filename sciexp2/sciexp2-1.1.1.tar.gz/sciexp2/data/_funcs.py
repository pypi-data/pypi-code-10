#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Data manipulation abstractions."""

from __future__ import print_function
from __future__ import absolute_import

__author__ = "Lluís Vilanova"
__copyright__ = "Copyright 2009-2014, Lluís Vilanova"
__license__ = "GPL version 3 or later"

__maintainer__ = "Lluís Vilanova"
__email__ = "vilanova@ac.upc.edu"


import collections
import functools
import numpy
import numpy as np                      # required for some numpy docstrings
from numpy.lib import recfunctions

from sciexp2.data import Data, data_array, _get_axis
from sciexp2.data import meta


##################################################
# * Concatenate / append

_numpy_concatenate = numpy.concatenate


@functools.wraps(numpy.concatenate)
def concatenate(arrays, axis=0):
    # check all-Data
    is_data = [(i, a) for i, a in enumerate(arrays)
               if isinstance(a, Data)]

    if len(is_data) > 0:
        _, axis = _get_axis(axis, [[a for i, a in is_data][0]])

    if len(is_data) == 0:
        # let it fail
        return _numpy_concatenate(arrays, axis)
    elif len(is_data) < len(arrays):
        is_nondata = [(i, a) for i, a in enumerate(arrays)
                      if not isinstance(a, Data)]
        msg = "Incompatible concatenate between "
        msg += "data (%d) and non-data (%d) arrays"
        raise TypeError(msg % (is_data[0][0], is_nondata[0][0]))

    if axis is None:
        raise ValueError("Cannot concatenate with 'axis' as None")
    elif axis > arrays[0].ndim:
        # let it fail
        try:
            _numpy_concatenate(arrays, axis=axis)
        except:
            raise
        # should never get here
        assert False

    # check compatibility
    for i, arr in enumerate(arrays):
        if arr.ndim != arrays[0].ndim:
            raise ValueError("all the input arrays must have same number of "
                             "dimensions")
        for didx in range(arr.ndim):
            if arr.dims[didx].expression != arrays[0].dims[didx].expression:
                raise ValueError("Incompatible expression "
                                 "for array %d in dimension %d" % (i, didx))
            if didx != axis and\
               list(arr.dims[didx]) != list(arrays[0].dims[didx]):
                raise ValueError("Incompatible contents "
                                 "for array %d in dimension %d" % (i, didx))

    arr_res = _numpy_concatenate(arrays, axis=axis)
    dims = []
    for didx in range(arrays[0].ndim):
        if didx == axis:
            dim_elems = []
            for arr in arrays:
                dim_elems.extend(arr.dims[didx])
            dims.append((arrays[0].dims[didx].expression, dim_elems))
        else:
            dims.append((arrays[0].dims[didx].expression,
                         list(arrays[0].dims[didx])))
    return data_array(arr_res, dims=dims, dtype=arr_res.dtype)


@functools.wraps(numpy.append)
def append(arr, values, axis=0):
    if not isinstance(arr, Data):
        raise TypeError("Cannot append into non-Data")
    if not isinstance(values, Data):
        raise TypeError("Cannot append non-Data")
    _, axis = _get_axis(axis, [arr])
    return concatenate((arr, values), axis=axis)


######################################################################
# * Fields management

def append_fields(base, names, data=None, dtypes=None, fill_value=-1):
    """Return a new array with additional fields.

    See also
    --------
    numpy.lib.recfunctions.append_fields

    """
    reference = [base]
    numpy_base = base.view(numpy.ndarray) \
                 if isinstance(base, Data) else base
    if isinstance(data, Data):
        reference += [data]
        numpy_data = data.view(numpy.ndarray).flat
    elif isinstance(data, collections.Iterable) and\
         not isinstance(data, numpy.ndarray):
        reference += data
        numpy_data = []
        for d in data:
            if isinstance(d, Data):
                d = d.view(numpy.ndarray)
            numpy_data.append(d)
    elif data is not None:
        reference += data
        numpy_data = data
    else:
        numpy_data = None

    res = recfunctions.append_fields(
        base=numpy_base, names=names, data=numpy_data,
        dtypes=dtypes, fill_value=fill_value,
        usemask=False, asrecarray=True)

    dims = None
    for arr in reference:
        if isinstance(arr, Data) and \
           reduce(int.__mul__, arr.shape) == reduce(int.__mul__, res.shape):
            dims = arr
            res = res.reshape(arr.shape)
            break
    if dims is None:
        raise ValueError("No input Data matches output shape (%s)" % res.shape)
    return data_array(res, dims=dims)


def drop_fields(base, drop_names):
    """Return a new array with fields in `drop_names` dropped.

    See also
    --------
    numpy.lib.recfunctions.drop_fields

    """
    if not isinstance(base, Data):
        raise TypeError("Not a Data array")
    res = recfunctions.drop_fields(
        base=base, drop_names=drop_names,
        usemask=False, asrecarray=True)
    return data_array(res, dims=base)


def rename_fields(base, namemapper):
    """Rename the fields from a flexible-datatype Data array.

    See also
    --------
    numpy.lib.recfunctions.rename_fields

    """
    if not isinstance(base, Data):
        raise TypeError("Not a Data array")
    res = recfunctions.rename_fields(
        base=base, namemapper=namemapper)
    return data_array(res, dims=base)


def merge_arrays(seqarrays, fill_value=-1, flatten=False):
    """Merge arrays field by field.

    See also
    --------
    numpy.lib.recfunctions.merge_arrays

    """
    res = recfunctions.merge_arrays(
        seqarrays=seqarrays, fill_value=fill_value, flatten=flatten,
        usemask=False, asrecarray=True)

    dims = None
    for arr in seqarrays:
        if isinstance(arr, Data) and \
           reduce(int.__mul__, arr.shape) == reduce(int.__mul__, res.shape):
            dims = arr
            res = res.reshape(arr.shape)
            break
    if dims is None:
        raise ValueError("No input Data matches output shape (%s)" % res.shape)
    return data_array(res, dims=dims)


######################################################################
# * Miscellaneous

@functools.wraps(numpy.copy)
def copy(a, order="C"):
    try:
        func = a.__class__.copy
    except AttributeError:
        func = numpy.copy
    return func(a, order=order)


@functools.wraps(numpy.imag)
def imag(val):
    try:
        func = val.__class__.imag
    except AttributeError:
        func = numpy.imag
    return func(val)


@functools.wraps(numpy.real)
def real(val):
    try:
        func = val.__class__.real
    except AttributeError:
        func = numpy.real
    return func(val)


@functools.wraps(numpy.ravel)
def ravel(a, order="C"):
    try:
        func = a.__class__.ravel
    except AttributeError:
        func = numpy.ravel
    return func(a, order=order)


@functools.wraps(numpy.delete)
def delete(arr, obj, axis=None):
    if not isinstance(arr, Data):
        raise TypeError("Not a Data array")
    _, axis = _get_axis(axis, [arr])
    if arr.ndim > 1 and axis is None:
        arr = arr.flatten(order="A")

    daxis = axis if axis is not None else 0
    obj = arr.dims[daxis]._get_indexes(obj)

    res = numpy.delete(arr, obj, axis)
    dims = [(dim.expression, dim)
            for dim in arr._dims]
    if axis is None:
        axis = 0
    dims[axis] = (dims[axis][0],
                  list(numpy.delete(list(dims[axis][1]), obj)))
    dims = [meta.Dim(dim[0], dim[1])
            for dim in dims]
    return data_array(res, dims=dims)


__all__ = [
    "concatenate", "append",
    "append_fields", "drop_fields", "rename_fields", "merge_arrays",
    "copy",
    "ravel",
    "delete",
]
