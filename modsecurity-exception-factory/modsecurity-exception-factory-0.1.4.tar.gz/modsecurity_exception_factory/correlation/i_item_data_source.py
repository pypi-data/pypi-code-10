#-*- coding: utf-8 -*-
#
# Created on Jan 15, 2013
#
# @author: Younes JAAIDI
#
# $Id: 6ef0ba3882870cd2b39e789c6f9361c125e5c41f $
#

from abc import abstractmethod

class IItemDataSource:

    @abstractmethod
    def itemDictIterable(self, variableNameList):
        raise NotImplementedError()
