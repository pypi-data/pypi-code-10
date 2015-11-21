from __future__ import absolute_import, division, print_function
import random
import collections
import uuid

import numpy as np

import scicfg
import environments as envs

import dotdot
from explorers import tools


class RandomEnv(envs.Environment):

    def __init__(self, mbounds):
        self.m_channels = [envs.Channel('m{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [envs.Channel('s0', ( 0.,  1.)),
                           envs.Channel('s1', (-1.,  1.)),
                           envs.Channel('s2', ( 3., 10.))]


    def _execute(self, m_signal, meta=None):
        return tools.random_signal(self.s_channels)

class RandomLinear(RandomEnv):

    def __init__(self, m_bounds, s_dim):
        self.m = np.random.random((len(m_bounds), s_dim))

        self.m_channels = [envs.Channel('order{}'.format(i), mb_i) for i, mb_i in enumerate(m_bounds)]
        self.s_channels = [envs.Channel('feedback{}'.format(i)) for _ in range(s_dim)]

    def _execute(self, m_signal, meta=None):
        m_vector = np.array([[m_signal[c.name] for c in self.m_channels]])
        s_vector = ((self.m*m_vector.T).T)[0]
        s_signal = tools.to_signal(s_vector, s_channels)

        return s_signal


class SimpleEnv(RandomEnv):

    def __init__(self):
        m_bounds = ((0.0, 1.0), (0.0, 1.0))
        self.m_channels = [envs.Channel(i, mb_i) for i, mb_i in enumerate(m_bounds)]
        self.s_channels = [envs.Channel(i) for i in enumerate((2, 3))]

    def _execute(self, m_signal, meta=None):
        m_vector = tools.to_vector(m_signal, self.m_channels)
        s_vector = (m_vector[0] + m_vector[1], m_vector[0]*m_vector[1])

        return tools.to_signal(s_vector, self.s_channels)


class BoundedRandomEnv(RandomEnv):

    def __init__(self, mbounds, sbounds):
        self.m_channels = [envs.Channel('m{}'.format(i), mb_i) for i, mb_i in enumerate(mbounds)]
        self.s_channels = [envs.Channel('s{}'.format(i), sb_i) for i, sb_i in enumerate(sbounds)]


assert issubclass(RandomEnv, envs.Environment)
assert issubclass(BoundedRandomEnv, envs.Environment)
