"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .. import tools
from .. import meshgrid
from . import s_mesh


defcfg = s_mesh.MeshgridGoalExplorer.defcfg._deepcopy()
defcfg._pop('cutoff')
defcfg._describe('max_effects', instanceof=numbers.Integral, default=1)
defcfg._describe('max_goals',   instanceof=numbers.Integral, default=100000000000)
defcfg.classname = 'explorers.FrontierGoalExplorer'


class FrontierGoalExplorer(s_mesh.MeshgridGoalExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(FrontierGoalExplorer, self).__init__(cfg, **kwargs)
        self._goal_meshgrid = meshgrid.MeshGrid(self.cfg, [c.bounds for c in self.s_channels])

    def _max_goals(self, coo):
        if not coo in self._goal_meshgrid._bins:
            return True
        else:
            b = self._goal_meshgrid._bins[coo]
            if len(b) <= self.cfg.max_goals:
                return True
        return False

    def _choose_goal(self):
        s_bins = self._meshgrid._nonempty_bins
        if len(s_bins) == 0:
            return None #s_goal = tools.random_signal(self.s_channels)
        else:
            s_bin = random.choice(s_bins)
            coo = s_bin.coo
            dim       = random.randint(0, len(coo)-1)
            direction = random.choice([-1, 1])
            s_goal = None
            while s_goal is None:
                coo = list(coo)
                coo[dim] += direction
                coo, flag = tuple(coo), False
                try:
                    b = self._meshgrid._bins[coo]
                    if len(b) <= self.cfg.max_effects:
                        flag = self._max_goals(coo)
                except KeyError:
                    flag = self._max_goals(coo)
                if flag:
                    s_bounds = self._meshgrid._bounds(coo)
                    s_goal   = tools.random_signal(self.s_channels, s_bounds)

            return s_goal

    def _explore(self):
        # pick a random bin
        s_goal   = self._choose_goal()
        m_signal = self._inv_request(s_goal)
        return {'m_signal': m_signal, 's_goal': s_goal, 'from': 'goal.babbling.unreach'}

    def receive(self, exploration, feedback):
        super(FrontierGoalExplorer, self).receive(exploration, feedback)
        if 's_goal' in exploration:
            self._goal_meshgrid.add(tools.to_vector(exploration['s_goal'], self.s_channels))
