#-*- coding: utf-8 -*-
#
# Created on Jan 8, 2013
#
# @author: Younes JAAIDI
#
# $Id: a09f9a043f200d4677673832392e25d8c8d56d84 $
#

from abc import abstractmethod
from ..correlation import IItemDataSource

class IModsecurityAuditDataSource(IItemDataSource):
    
    @abstractmethod
    def insertModsecurityAuditEntryIterable(self, modsecurityAuditEntryIterable):
        raise NotImplementedError()

    @abstractmethod
    def variableValueIterable(self, columnName):
        raise NotImplementedError()

    @abstractmethod
    def itemDictIterable(self, variableNameList):
        raise NotImplementedError()

    @abstractmethod
    def orangeDataReader(self):
        raise NotImplementedError()
