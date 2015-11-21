"""\
"""
from __future__ import absolute_import, division, print_function
import collections
import math

import shapely
import shapely.ops

from .. import tools
from .. import meshgrid


class Diversity(object):

    def __init__(self, cfg):
        self.cfg = cfg
        self.s_channels = self.cfg.s_channels

    def add(self, ex_uuids, s_signal):
        """Return the diversity value of s_signal"""
        raise NotImplementedError

    @property
    def diversity(self):
        """Return the diversity history per strategy"""
        raise NotImplementedError


class DiversityGrid(Diversity):

    def __init__(self, cfg, ex_uuids):
        super(DiversityGrid, self).__init__(cfg)
        self._meshgrid = meshgrid.ExplorerMeshGrid(self.cfg, self.s_channels)
        self._diversity = {ex_uuid: collections.deque([1.0 for _ in range(self.cfg.head_start)],
                                                      self.cfg.window)
                           for ex_uuid in ex_uuids}

    def add(self, ex_uuids, s_signal):
        """The diversity value decreases (with gamma < 1) when the grid cell is populated"""
        coo  = self._meshgrid.add(s_signal)
        cell = self._meshgrid.bins[coo]
        w = self.cfg.gamma**(len(cell)-1)
        for ex_uuid in ex_uuids:
            try:
                self._diversity[ex_uuid].append(w)
            except KeyError: # the explorer is not amongst the selectable one
                pass
        return w

    @property
    def diversity(self):
        return {ex_uuid: sum(dw)/max(1, len(dw)) for ex_uuid, dw in self._diversity.items()}


import random

class DiversityHyperBall(Diversity):

    def __init__(self, cfg, ex_uuids):
        super(DiversityHyperBall, self).__init__(cfg)
        assert len(cfg.s_channels) == 2
        self._diversity = {ex_uuid: collections.deque([math.pi*self.cfg.threshold**2
                                                       for _ in range(self.cfg._get('head_start', 0))],
                                                       self.cfg._get('window', 1))
                           for ex_uuid in ex_uuids}
        self._coverage = shapely.geometry.MultiPolygon([])

    def add(self, ex_uuids, s_signal):
        """The diversity value is the added volume of the hyperballs"""
        old_area = self._coverage.area
        s_vector = tools.to_vector(s_signal, self.s_channels)
        self._coverage = self._coverage.union(shapely.geometry.Point(s_vector).buffer(self.cfg.threshold))
        w = self._coverage.area - old_area
        for ex_uuid in ex_uuids:
            try:
                self._diversity[ex_uuid].append(w)
            except KeyError: # the explorer is not amongst the selectable one # FIXME: what about selecting composite explorers ?
                pass
        return w

    @property
    def diversity(self):
        return {ex_uuid: sum(dw)/max(1, len(dw)) for ex_uuid, dw in self._diversity.items()}
