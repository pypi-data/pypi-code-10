# -*- coding:utf-8 -*-
from __future__ import unicode_literals


class BaseAPI(object):
    """
    百度 API 基类
    """
    scope = ''
    version = ''

    def __init__(self, client=None):
        self.__client = client

    @property
    def base_url(self):
        return '{api_host}/{scope}/{version}'.format(
            api_host=self.__client.api_host,
            scope=self.scope,
            version=self.version
        ).rstrip('/')

    def post(self, url, **kwargs):
        url = self.base_url + url
        return self.__client.post(url, **kwargs)

    def get(self, url, **kwargs):
        url = self.base_url + url
        return self.__client.get(url, **kwargs)
