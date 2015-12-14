# -*- coding:utf-8 -*-
from __future__ import unicode_literals


class BaiduException(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __unicode__(self):
        return '<BaiduException {0}>'.format(self.errcode)


class GeotableDoesNotExistException(BaiduException):
    def __init__(self):
        super(BaiduException, self).__init__(1004, 'geotable不存在')

    def __unicode__(self):
        return '<GeotableDoesNotExistException {0}>'.format(self.errcode)
