from __future__ import absolute_import, division, print_function
import unittest
import random

import learners

import dotdot
import explorers

import testenvs

class TestMeshgridGoalExplorer(unittest.TestCase):

    def test_s_rand(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = explorers.MeshgridGoalExplorer.defcfg._deepcopy()
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels
        exp_cfg.learner = learners.RandomLearner.defcfg._deepcopy()
        exp_cfg.res = 100

        exp = explorers.MeshgridGoalExplorer(exp_cfg)

        for _ in range(10):
            m_signal = explorers.tools.random_signal(env.m_channels)
            exploration = {'m_signal': m_signal}
            feedback = env.execute(exploration)
            exp.receive(exploration, feedback)


        for t in range(100):
            exploration = exp.explore()
            print(exploration)
            explorers.tools.signal_inbound(exploration['m_signal'], env.m_channels)
#            self.assertTrue(all(c.bounds[0] <= exploration['m_signal'][c.name] <= c.bounds[1] for c in env.m_channels))
            feedback = env.execute(exploration)
            exp.receive(exploration, feedback)

if __name__ == '__main__':
    unittest.main()
