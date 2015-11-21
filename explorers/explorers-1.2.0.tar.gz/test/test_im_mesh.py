from __future__ import absolute_import, division, print_function
import unittest
import random

import scicfg

import dotdot
import learners
import explorers
from explorers import tools

import testenvs

class TestIMExplorer(unittest.TestCase):

    def test_im(self):

        mbounds = ((23, 34), (-3, -2))
        sbounds = ((0, 1), (-1, -0), (101, 1001))
        env = testenvs.BoundedRandomEnv(mbounds, sbounds)
        exp_cfg = explorers.IMExplorer.defcfg._deepcopy()
        exp_cfg.m_channels = env.m_channels
        exp_cfg.s_channels = env.s_channels
        exp_cfg.learner = learners.RandomLearner.defcfg._deepcopy()
        exp_cfg.res = 100

        for im_name in ['explorers.LocalInterestModel',
                        'explorers.PredictiveNoveltyMotivation',
                        'explorers.IntermediateLevelOfNoveltyMotivation',
                       ]:
            exp_cfg.lim.classname = im_name

            exp = explorers.IMExplorer(exp_cfg)

            for t in range(10):
                m_signal = tools.random_signal(env.m_channels)
                feedback = env.execute(m_signal)
                exp.receive({'m_signal': m_signal, 'uuid': exp.cfg.uuid}, feedback)

            for t in range(100):
                exploration = exp.explore()
                self.assertTrue(all(c.bounds[0] <= exploration['m_signal'][c.name] <= c.bounds[1] for c in env.m_channels))
                feedback = env.execute(exploration['m_signal'])
                exp.receive(exploration, feedback)


if __name__ == '__main__':
    unittest.main()
