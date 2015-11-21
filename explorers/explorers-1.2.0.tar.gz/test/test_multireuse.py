from __future__ import absolute_import, division, print_function
import unittest
import random

import scicfg

import dotdot
import explorers
from explorers import Channel, tools

import testenvs

random.seed(0)

class TestMultiReuse(unittest.TestCase):

    def test_multi_random(self):
        mbounds = ((0, 1), (-1, 0))
        sbounds = ((4, 9),)

        env = testenvs.RandomEnv(mbounds)

        reuse_cfg                  = explorers.MultiReuseExplorer.defcfg._deepcopy()
        reuse_cfg.m_channels       = env.m_channels
        reuse_cfg.s_channels       = env.m_channels
        reuse_cfg.reuse.s_channels = env.s_channels
        reuse_cfg.reuse.algorithm  = 'random'
        reuse_cfg.reuse.res        = 10
        reuse_cfg.pick_algorithm   = 'diversity'
        reuse_cfg.res              = 10
        reuse_cfg._strict(True)

        datasets = []
        orders  = []
        for _ in range(5):
            dataset = {'m_channels'  : env.m_channels,
                       's_channels'  : env.s_channels,
                       'explorations': []}
            for _ in range(100):
                m = tools.random_signal(reuse_cfg.m_channels)
                s = tools.random_signal(reuse_cfg.reuse.s_channels)
                dataset['explorations'].append(({'m_signal': m}, {'s_signal': s}))
                orders.append(m)

            datasets.append(dataset)


        reuse_explorer = explorers.MultiReuseExplorer(reuse_cfg, datasets)

        print(reuse_explorer.cfg)

        for _ in range(500):
            order = reuse_explorer.explore()
            self.assertTrue(order['m_signal'] in orders)

        self.assertEqual(reuse_explorer.explore(), None)

if __name__ == '__main__':
    unittest.main()
