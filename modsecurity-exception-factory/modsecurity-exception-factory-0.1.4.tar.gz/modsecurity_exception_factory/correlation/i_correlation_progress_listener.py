#-*- coding: utf-8 -*-
#
# Created on Feb 15, 2013
#
# @author: rm4dillo
#
# $Id: 02243a342ce7bb14bd19ce5217f01ef18b9d2286 $
#

from abc import abstractmethod

class ICorrelationProgressListener:

    @abstractmethod
    def progress(self, correlatedCount, totalCount):
        raise NotImplementedError()
