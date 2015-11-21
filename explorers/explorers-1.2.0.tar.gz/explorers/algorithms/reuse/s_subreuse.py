"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers

from . import s_reusegen
from . import s_reuse
from ... import tools


defcfg = s_reuse.ReuseExplorer.defcfg._deepcopy()
defcfg.classname = 'explorers.SubReuseExplorer'


class SubReuseExplorer(s_reuse.ReuseExplorer):
    """A reuse explorer that can exploit dataset whose motor channels
    only overlap the one of the explorer partially.
    """

    defcfg = defcfg

    def __init__(self, cfg, datasets=(), **kwargs):
        super(SubReuseExplorer, self).__init__(cfg, datasets=datasets, **kwargs)
        self.s_random_channels = [c for c in self.m_channels
                                  if c not in self.reuse_generator.cfg.reuse.m_channels]

    def _explore(self):
        try:
            m_signal_reuse = next(self.reuse_generator)
            m_signal_rand  = tools.random_signal(self.s_random_channels)
            m_signal = tools.merge_signals(m_signal_reuse, m_signal_rand)
            return {'m_signal': m_signal}
        except StopIteration:
            return None
