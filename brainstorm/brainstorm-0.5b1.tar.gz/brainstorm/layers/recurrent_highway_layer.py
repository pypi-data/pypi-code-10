#!/usr/bin/env python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from collections import OrderedDict

from brainstorm.layers.base_layer import Layer
from brainstorm.structure.buffer_structure import (BufferStructure,
                                                   StructureTemplate)
from brainstorm.structure.construction import ConstructionWrapper
from brainstorm.utils import LayerValidationError


def RecurrentHighway(name=None):
    """Create a Recurrent Highway layer."""
    return ConstructionWrapper.create(RecurrentHighwayLayerImpl, name=name)


class RecurrentHighwayLayerImpl(Layer):
    expected_inputs = {'H': StructureTemplate('T', 'B', '...'),
                       'I': StructureTemplate('T', 'B', '...')}

    def setup(self, kwargs, in_shapes):
        # 'H' and 'I' must have the same shape
        if in_shapes['H'] != in_shapes['I']:
            raise LayerValidationError(
                "{}: H and T must have the same shape but got {} and {}"
                .format(self.name, in_shapes['H'], in_shapes['I']))

        outputs = OrderedDict()
        outputs['default'] = BufferStructure(
            'T', 'B', *self.in_shapes['H'].feature_shape)
        return outputs, OrderedDict(), OrderedDict()

    def forward_pass(self, buffers, training_pass=True):
        # prepare
        _h = self.handler
        H = buffers.inputs.H
        I = buffers.inputs.I
        y = buffers.outputs.default

        tmp = _h.zeros(H[0].shape)
        for t in range(H.shape[0]):
            _h.subtract_tt(H[t], y[t - 1], out=tmp)
            _h.mult_tt(I[t], tmp, out=tmp)
            _h.add_tt(tmp, y[t - 1], out=y)

    def backward_pass(self, buffers):
        # prepare
        _h = self.handler
        H = buffers.inputs.H
        I = buffers.inputs.I
        dH = buffers.input_deltas.H
        dI = buffers.input_deltas.I
        dy = buffers.output_deltas.default

        T = H.shape[0] - 1
        tmp = _h.ones(dx[0].shape)
        for t in range(T - 1, -1, -1):
            _h.subtract_tt(tmp, I[t], out=tmp)
            _h.mult_add_tt(tmp, dy[t], out=dx)

            _h.mult_add_tt(I[t], dy[t], out=dH)

            _h.subtract_tt(H[t], x[t], out=tmp)
            _h.mult_add_tt(tmp, dy[t], out=dI)
