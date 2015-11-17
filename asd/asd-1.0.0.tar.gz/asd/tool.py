
from abc import ABCMeta, abstractmethod

class ToolBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(self, parser):
        pass

    @abstractmethod
    def process(self, args):
        pass
