"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections
import numbers

import numpy as np

from .. import Explorer
from .. import tools

from .diversities import DiversityGrid
from .diversities import DiversityHyperBall


div_algos = {'grid': DiversityGrid,
             'hyperball': DiversityHyperBall}


defcfg = Explorer.defcfg._deepcopy()
defcfg.classname = 'explorers.AdaptExplorer'
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._describe('div_algorithm', instanceof=str,
                 docstring='algorithm for calculating diversity')
defcfg._describe('diversity_power', instanceof=numbers.Real, default=1.0,
                 docstring='the diverisity value will be brough to ')
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg._describe('gamma', instanceof=numbers.Real, default=0.5,
                 docstring='gamma factor for cell value')
defcfg._describe('threshold', instanceof=numbers.Real,
                 docstring='threshold for hyperball coverage')
defcfg._describe('window', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='how much into the past to consider')
defcfg._describe('random_ratio', instanceof=numbers.Real,
                 docstring='how often explorers are choosen regardless of weight')
defcfg._describe('head_start', instanceof=numbers.Integral, default=0,
                 docstring='how much fake diversity hit to attribute at the beginning')
defcfg._describe('fallback', instanceof=(numbers.Integral), default=-1,
                 docstring='The explorer to fallback on if the chosen one returned None. Its value will be returned even if equal to None.')
defcfg._describe('weight_history', instanceof=bool, default=True,
                 docstring='Save the weight history')
#defcfg._branch('ex_0') # first explorer
#defcfg._branch('ex_1') # second explorer


class AdaptExplorer(Explorer):
    """\
    An explorer to select other explorers based on the diversity (new cells) they discover
    """

    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(AdaptExplorer, self).__init__(cfg, **kwargs)

        self._create_subexplorers(**kwargs)

        ex_uuids = tuple(ex.uuid for ex in self.explorers)
        self._diversity = div_algos[cfg.div_algorithm](self.cfg, ex_uuids)

        self.weight_history = {'ex_names': tuple(ex.name for ex in self.explorers),
                               'ex_uuids': ex_uuids,
                               'data'    : []}
        self.t = 0

    def _create_subexplorers(self, **kwargs):
        self.explorers = []
        self._ex_map   = {}

        idx = 0
        while idx != -1:
            try:
                ex_cfg = self.cfg['ex_{}'.format(idx)]
                ex_cfg._setdefault('m_channels', self.cfg.m_channels)
                assert 's_channels' in self.cfg
                if 's_channels' in self.cfg:
                    ex_cfg._setdefault('s_channels', self.cfg.s_channels)
                ex = Explorer.create(ex_cfg, **kwargs)
                self.exp_conduit.register(ex.receive)
                self.explorers.append(ex)
                self._ex_map[ex.uuid] = ex
                idx += 1
            except KeyError:
                idx = -1

        self.ex_uuids  = tuple(ex.uuid for ex in self.explorers)
        self.ex_names  = tuple(ex.name for ex in self.explorers)



    @property
    def weights(self):
        return tuple(sum(dw)/max(1, len(dw)) for dw in self._diversities)

    def _explore(self):
        if self.cfg.weight_history: # logging diversity history
            div_map = self._diversity.diversity
            if len(div_map) >= 1:
                div_list = np.array([div_map[ex_uuid] for ex_uuid in self.ex_uuids])
                self.weight_history['data'].append(div_list)
        if random.random() < self.cfg.random_ratio:
            idx = random.choice(range(len(self.explorers)))
        else:
            if not self.cfg.weight_history:
                div_map = self._diversity.diversity
            if len(div_map) >= 1:
                if not self.cfg.weight_history:
                    div_list = np.array([div_map[ex_uuid] for ex_uuid in self.ex_uuids])
                idx = tools.roulette_wheel(div_list**self.cfg.diversity_power)
            else:
                idx = random.choice(range(len(self.explorers)))



        exploration = self.explorers[idx].explore()
        if exploration is None and self.cfg.fallback != -1:
            return self.explorers[self.cfg.fallback].explore()
        return exploration

    def receive(self, exploration, feedback):
        super(AdaptExplorer, self).receive(exploration, feedback)
        self._diversity.add(exploration['uuids'], feedback['s_signal'])
