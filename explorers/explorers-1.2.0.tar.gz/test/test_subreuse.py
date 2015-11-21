from __future__ import absolute_import, division, print_function
import unittest
import random

import scicfg

import dotdot
import explorers
import learners

import environments as envs
from explorers import tools

import testenvs


random.seed(0)


class TestSubReuse(unittest.TestCase):

    def test_subreuse(self):
            mbounds = ((0, 1), (-1, 0))
            sbounds = ((4, 9),)

            env = testenvs.RandomEnv(mbounds)

            reuse_cfg                  = explorers.SubReuseExplorer.defcfg._deepcopy()
            reuse_cfg.m_channels       = env.m_channels
            reuse_cfg.reuse.s_channels = env.s_channels
            reuse_cfg.reuse.algorithm  = 'random'
            reuse_cfg.reuse.res        = 10
            reuse_cfg._strict(True)


            dataset = {'m_channels'  : [env.m_channels[0]],
                       's_channels'  : env.s_channels,
                       'explorations': []}
            orders  = []
            for _ in range(100):
                m = tools.random_signal(reuse_cfg.m_channels)
                m.pop(env.m_channels[1].name)
                s = tools.random_signal(reuse_cfg.reuse.s_channels)
                dataset['explorations'].append(({'m_signal': m}, {'s_signal': s}))
                orders.append(m)

            reuse_explorer = explorers.SubReuseExplorer(reuse_cfg, [dataset])

            for _ in range(100):
                order = reuse_explorer.explore()
                order['m_signal'].pop(env.m_channels[1].name)
                self.assertTrue(order['m_signal'] in orders)

            self.assertEqual(reuse_explorer.explore(), None)


if __name__ == '__main__':
    unittest.main()
