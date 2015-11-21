from __future__ import absolute_import, division, print_function, unicode_literals
import unittest
import random

import scicfg

import dotdot
import explorers

import testenvs

class TestRandomMotorExplorer(unittest.TestCase):

    def test_random(self):

        mbounds = ((23, 34), (-3, -2), (0, 1))
        env = testenvs.RandomEnv(mbounds)
        exp_cfg = scicfg.SciConfig()
        exp_cfg.m_channels = env.m_channels

        exp = explorers.RandomMotorExplorer(exp_cfg)

        for t in range(100):
            order = exp.explore()
            self.assertEqual(order['from'], 'motor.babbling')
            self.assertTrue(all(c.bounds[0] <= order['m_signal'][c.name] <= c.bounds[1] for c in env.m_channels))
            feedback = env.execute(order['m_signal'])
            exp.receive(order, feedback)

    def test_simple(self):

        env = testenvs.SimpleEnv()
        exp_cfg = scicfg.SciConfig()
        exp_cfg.m_channels = env.m_channels

        exp = explorers.RandomMotorExplorer(exp_cfg)

        for t in range(100):
            order = exp.explore()
            self.assertEqual(order['from'], 'motor.babbling')
            self.assertTrue(all(c.bounds[0] <= order['m_signal'][c.name] <= c.bounds[1] for c in env.m_channels))
            feedback = env.execute(order['m_signal'])
            exp.receive(order, feedback)


if __name__ == '__main__':
    unittest.main()
