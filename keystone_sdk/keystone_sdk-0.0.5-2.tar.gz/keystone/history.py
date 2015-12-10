# -*- coding: utf-8 -*-

from collections import deque, Iterable
import pandas as pd

import keystone.utils
from keystone.api import keystone_class, api_method
from keystone.coordinator import KSObserver
import datetime


class KSHistory(KSObserver):
    def __init__(self, capacity):
        if not keystone.utils.isint(capacity) or capacity == 0:
            raise TypeError(u"capacity格式错误，capacity必须为非0整数。".encode('utf8'))
        self.__capacity = capacity
        self.__data = deque([],capacity)
        
    
    def query(self, startTime, endTime, ids, fieldname):
        # print "[startTime,endTime] = [" + str(startTime) + "," + str(endTime) +"]"
        # Check parameters
        if not isinstance(startTime, datetime.datetime):
            raise TypeError(u"startTime格式错误，startTime必须为datetime类型。".encode('utf8'))
        
        if not isinstance(endTime, datetime.datetime):
            raise TypeError(u"endTime格式错误，endTime必须为datetime类型。".encode('utf8'))
        
        if not isinstance(fieldname, str):
            raise TypeError(u"fieldname格式错误, fieldname必须是字符串。".encode('utf8'))
        
        if not isinstance(ids, str) and not isinstance(ids, Iterable):
            raise TypeError(u"securities格式错误, securities必须是字符串或字符串数组。".encode('utf8'))
        
        if isinstance(ids, Iterable):
            for x in ids:
                if not isinstance(x, str):
                        raise TypeError(u"securities格式错误, securities必须是字符串或字符串数组。".encode('utf8'))
        
        # Query
        ret = pd.DataFrame()
        for dataEvent in self.__data:
            dt = dataEvent.time()
            if startTime <= dt and dt <= endTime:
                ret = ret.join(dataEvent.query(ids, fieldname), how = 'outer')
                
        return ret
    
    
    def queryN(self, n, ids, fieldname):
        # Check parameters
        if not keystone.utils.isint(n) or n == 0:
            raise TypeError(u"n格式错误，n必须为非0整数。".encode('utf8'))
        
        if not isinstance(fieldname, str):
            raise TypeError(u"fieldname格式错误, fieldname必须是字符串。".encode('utf8'))
        
        if not isinstance(ids, str) and not isinstance(ids, Iterable):
            raise TypeError(u"securities格式错误, securities必须是字符串或字符串数组。".encode('utf8'))
        
        if isinstance(ids, Iterable):
            for x in ids:
                if not isinstance(x, str):
                        raise TypeError(u"securities格式错误, securities必须是字符串或字符串数组。".encode('utf8'))
                    
        # QueryN
        ret = pd.DataFrame()
        m = min(n, len(self.__data))
        iter = xrange(len(self.__data) - m, len(self.__data))
        for i in iter:
            ret = ret.join(self.__data[i].query(ids, fieldname), how = 'outer')
            
        return ret
    
    def onDataEvent(self, dataEvent):
        self.__data.append(dataEvent)
    