from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import random

import scicfg

import dotdot
import explorers
import learners

import testenvs

class TestRandomMotorExplorer(unittest.TestCase):

    def test_random(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)

        exp_cfg  = explorers.MetaExplorer.defcfg._deepcopy()
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels
        exp_cfg.ex_0 = explorers.RandomMotorExplorer.defcfg._deepcopy()
        exp_cfg.ex_1 = explorers.RandomGoalExplorer.defcfg._deepcopy()
        exp_cfg.ex_1.learner = learners.RandomLearner.defcfg._deepcopy()

        exp_cfg.eras = [10, 50, 100]
        exp_cfg.weights = [[1.0, 0.0], [0.3, 0.7], [0.0, 1.0]]

        exp = explorers.Explorer.create(exp_cfg)

        for t in range(100):
            order = exp.explore()
            if t < 10:
                self.assertEqual(order['from'], 'motor.babbling')
            if t > 50:
                self.assertEqual(order['from'], 'goal.babbling')
            self.assertTrue(all(c.bounds[0] <= order['m_signal'][c.name] <= c.bounds[1] for c in env.m_channels))
            feedback = env.execute(order['m_signal'])
            exp.receive(order, feedback)


if __name__ == '__main__':
    unittest.main()
