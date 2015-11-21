from __future__ import absolute_import, division, print_function
import unittest
import random

import scicfg

import dotdot
from explorers.algorithms import reuse
from explorers import Channel, tools

random.seed(0)


class TestReuse(unittest.TestCase):

    def test_reuse_simple(self):
        m_channels = (Channel('a', (0, 1)), Channel('b', (-1, 0)))
        s_channels = (Channel('x', (4, 9)),)

        dataset = {'m_channels'  : m_channels,
                   's_channels'  : s_channels,
                   'explorations': []}
        orders  = []
        for _ in range(1000):
            m = tools.random_signal(m_channels)
            s = tools.random_signal(s_channels)
            dataset['explorations'].append(({'m_signal': m}, {'s_signal': s}))
            orders.append(m)

        reuse_cfg = reuse.s_reusegen.RandomReuse.defcfg._deepcopy()
        rndreuse = reuse.s_reusegen.RandomReuse(reuse_cfg, dataset)

        self.assertEqual(len(rndreuse), 1000)

        c = 0
        for mc in rndreuse:
            c += 1
            self.assertTrue(mc in orders)

        self.assertEqual(c, 1000)
        self.assertEqual(len(rndreuse), 0)


if __name__ == '__main__':
    unittest.main()
