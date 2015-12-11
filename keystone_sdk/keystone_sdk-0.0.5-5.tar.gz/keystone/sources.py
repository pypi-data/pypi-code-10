# -*- coding: utf-8 -*-

from keystone.engine import KSEventEngine
import time
import pandas as pd
import sys

class KSBaseSource(dict):
    ''' KSBaseSource for user data '''
    def tagAsPriceData(self, securityColumn, priceColumn):
        if not isinstance(securityColumn, basestring):
            raise TypeError(u"securityColumn格式错误, securityColumn必须是字符串。".encode('utf8'))
        if not isinstance(priceColumn, basestring):
            raise TypeError(u"priceColumn格式错误, priceColumn必须是字符串。".encode('utf8'))
        self['sid_column'] = securityColumn
        self['price_column'] = priceColumn

    def tagAsSecurityData(self, securityColumn):
        if not isinstance(securityColumn, basestring):
            raise TypeError(u"securityColumn格式错误, securityColumn必须是字符串。".encode('utf8'))
        self['sid_column'] = securityColumn

    def setDateFormat(self, dateFormat):
        if not isinstance(dateFormat, basestring):
            raise TypeError(u"dateFormat格式错误, dateFormat必须是字符串。".encode('utf8'))
        self['date_format'] = dateFormat

    def setDateColumn(self, dateColumn):
        if not isinstance(dateColumn, basestring):
            raise TypeError(u"dateColumn格式错误, dateColumn必须是字符串。".encode('utf8'))
        self['date_column'] = dateColumn

class KSCsvSource(KSBaseSource):
    def __init__(self, filename, dateColumn, dateFormat):
        KSBaseSource.__init__(self)
        self.setDateColumn(dateColumn)
        self.setDateFormat(dateFormat)
        self['type'] = "CSV"
        self['filename'] = filename

    def setDelimiter(self, delimiter):
        self['delimiter'] = delimiter
        
class KSMemorySource(KSBaseSource):
    def __init__(self):
        pass
    