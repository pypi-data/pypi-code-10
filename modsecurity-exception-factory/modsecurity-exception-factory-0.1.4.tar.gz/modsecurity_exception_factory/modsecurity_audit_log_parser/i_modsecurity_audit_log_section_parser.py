#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id: bde15b9d485f0f510409047423ea024d1b7689ab $
#

from abc import abstractmethod

class IModsecurityAuditLogSectionParser:
    
    @abstractmethod
    def parseLine(self, state):
        raise NotImplementedError()
