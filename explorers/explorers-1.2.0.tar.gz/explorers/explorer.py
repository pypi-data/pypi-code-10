"""\
Explorer base class
"""
from __future__ import absolute_import, division, print_function
import collections
import abc
import uuid

import scicfg

from . import conduits
from . import tools

defcfg = scicfg.SciConfig()
defcfg._describe('m_channels', instanceof=collections.Iterable,
                 docstring='Motor channels to generate random order of')
defcfg._describe('classname', instanceof=collections.Iterable,
                 docstring='The name of the explorer class. Only used with the create() class method.')
defcfg._describe('uuid', instanceof=str,
                 docstring='Uuid for the explorer. Allows to reload explorers consistent with saved explorations')
defcfg._describe('name', instanceof=str, default='',
                 docstring='Informal name for the explorer.')


class Explorer(object):
    """"""
    __metaclass__ = abc.ABCMeta

    defcfg = defcfg

    @classmethod
    def create(cls, cfg, **kwargs):
        class_ = tools._load_class(cfg.classname)
        return class_(cfg, **kwargs)

    def __init__(self, cfg, **kwargs):
        if isinstance(cfg, dict):
            cfg = scicfg.SciConfig(cfg)
        self.cfg = cfg
        self.cfg._update(self.defcfg, overwrite=False)

        self.cfg._setdefault('uuid', uuid.uuid4().hex)
        self.uuid = self.cfg.uuid

        self._m_channels = self.cfg.m_channels

        self.exp_conduit = conduits.UnidirectionalHub() # exploration (exploration and feedback, for receive())
        self.obs_conduit = conduits.UnidirectionalHub() # observation (only m_signal, s_signal, uuid for learners)
        self.fwd_conduit = conduits.BidirectionalHub()  # prediction requests
        self.inv_conduit = conduits.BidirectionalHub()  # inverse requests

    @property
    def name(self):
        if self.cfg.name == '':
            return self.__class__.__name__
        else:
            return self.cfg.name

    @property
    def m_channels(self):
        return self._m_channels

    # @m_channels.setter
    # def m_channels(self, channels):
    #     assert set(c.name for c in channels) == set(c.name for c in self.m_channels)
    #     self._m_channels = channels


    @property
    def s_channels(self): # note: not provided by all configurations necessarily.
        return self.cfg.s_channels

    def explore(self):
        """
            Wrapping function for self._explore()
            Checks and fill 'uuid' and 'from' field if not provided.
            # return {'m_signal': m_signal, # the actual motor command to try to execute in the environment.
            #         's_goal'  : s_signal, # if the motor command was generated a sensory goal, include this.
            #         'uuid'    : self.uuid,
            #         'from'    : 'exploration.strategy'}
        """
        exploration = self._explore()
        if exploration is None:
            return None
        else:
            assert 'm_signal' in exploration
            if 'uuids' not in exploration:
                exploration['uuids'] = []
            exploration['uuids'].append(self.uuid)
            if 'uuid' not in exploration: # will be deprecated
                exploration['uuid'] = self.uuid
            if 'from' not in exploration:
                exploration['from'] = self.name

            return exploration


    def receive(self, exploration, feedback):
        assert isinstance(exploration, dict)
        #assert 'uuids' in exploration # commented for backward compatibility purposes
        assert isinstance(feedback, dict) and 'uuid' in feedback

        obs_feedback = {'m_signal': exploration['m_signal'],
                        's_signal': feedback['s_signal'],
                        'uuid'    : feedback['uuid']}

        self.obs_conduit.receive(obs_feedback)
        self.exp_conduit.receive(exploration, feedback)
