"""\
Straightforwardly restrict the range of the motor channels.
Useful to create simple maturational constraints.
"""
from __future__ import absolute_import, division, print_function

import random
import collections

import learners

from .. import conduits
from .. import tools

from .. import RandomGoalExplorer

defcfg = RandomGoalExplorer.defcfg._deepcopy()
defcfg.classname = 'explorers.MotorConstraintGoalExplorer'
defcfg._decribe('virtual_m_bounds', default=None,
                 docstring='Define more constraining bounds on motor range')

class MotorConstraintGoalExplorer(explorer.Explorer):
    """\
    A goal babbling explorer with motor constraints.
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MotorConstraintGoalExplorer, self).__init__(cfg)

    def _explore(self):
        s_goal = tools.random_signal(self.s_channels)
        m_signal = self._inv_request(s_goal)
        if m_signal is None:
            m_signal = tools.random_signal(self.m_channels)
        return {'m_signal': m_signal, 's_goal': s_goal, 'from': 'goal.babbling'}

    def _inv_request(self, s_goal):
        orders = self.inv_conduit.poll({'s_goal': s_goal,
                                        'm_channels': self.m_channels})
        return None if len(orders) == 0 else random.choice(orders)

    def _fwd_request(self, m_signal):
        predictions = self.fwd_conduit.poll({'m_signal': m_signal,
                                             's_channels': self.s_channels})
        return None if len(predictions) == 0 else random.choice(predictions)
