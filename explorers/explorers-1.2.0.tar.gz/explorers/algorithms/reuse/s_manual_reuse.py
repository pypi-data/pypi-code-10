"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers

from ..m_rand import RandomMotorExplorer

defcfg = RandomMotorExplorer.defcfg._deepcopy()
defcfg.classname = 'explorers.ManualReuseExplorer'
defcfg._describe('dataset', instanceof=dict,
                 docstring='The dataset of motor command to reuse from')

class ManualReuseExplorer(RandomMotorExplorer):
    """A reuse explorer"""

    defcfg = defcfg

    def __init__(self, cfg, datasets=(), **kwargs):
        super(RandomMotorExplorer, self).__init__(cfg)

        assert len(datasets) == 1
        self._dataset = datasets[0]

        assert self.m_channels == self._dataset['m_channels']
        self.m_signals = iter(self._dataset['m_signals'])

    def _explore(self):
        try:
            m_signal = next(self.m_signals)
            return {'m_signal': m_signal}
        except StopIteration:
            return None
