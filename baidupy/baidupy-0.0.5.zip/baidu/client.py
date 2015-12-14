# -*- coding:utf-8 -*-
"""
结果原则：

1. api 操作成功， 去除 status和 message。
    - 如果有其他数据，直接返回
    - 如果有模型数据，转换成相应模型再返回；
    - 如果没有其他数据，返回 True
1. api 操作失败，将 status 和 message传入 BaiduException并抛出。
"""
from __future__ import unicode_literals
import inspect
from six.moves.urllib.parse import quote, quote_plus
import hashlib
import requests

from baidu.exceptions import BaiduException
from baidu.api.base import BaseAPI
from baidu.api.map.lbscloud import GeoDataAPI
from baidu.api.map.geosearch import GeoSearchAPI
from baidu.api.iplocation import IPLocationAPI
from baidu.api.geoconv import GeoConvAPI


def _is_api_endpoint(obj):
    return isinstance(obj, BaseAPI)


class BaseClient(object):

    safe_chars = "/:=&?#+!$,;'@()*[]"
    api_host = ''

    def __new__(cls, *args, **kwargs):
        self = super(BaseClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, ak, sk=None):
        self.__ak = ak
        if sk:
            self.__sk = sk
            self.model = 'sn'
        else:
            self.model = 'ip'

    def sn(self, query_str):
        """
        计算 sn
        """
        encoded_str = quote(query_str, safe=self.safe_chars)
        raw_str = encoded_str + self.__sk
        return hashlib.md5(quote_plus(raw_str).encode('utf-8')).hexdigest()

    def _request(self, method, url, **kwargs):
        if method == 'post':
            if 'data' not in kwargs:
                kwargs['data'] = {}
            kwargs['data']['ak'] = self.__ak
        elif method == 'get':
            if 'params' not in kwargs:
                kwargs['params'] = {}
            kwargs['params']['ak'] = self.__ak
        if self.model == 'sn':
            arg_list = []
            if 'params' in kwargs:
                for arg, value in kwargs['params'].items():
                    arg_list.append('{0}={1}'.format(arg, value))
            query_str = '&'.join(arg_list)
            url = '{url}?{params}'.format(url=url, params=query_str)
            query_str1 = url[len(self.api_host):]
            sn = self.sn(query_str1)
            url += '&sn={sn}'.format(sn=sn)
            kwargs['params'] = {}

        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException:
            raise BaiduException(
                errcode=10000,
                errmsg='未知异常',
            )

        return self._handle_result(res, method, url, **kwargs)

    def _handle_result(self, res, method=None, url=None, **kwargs):
        res.encoding = 'utf-8'
        try:
            result = res.json()
        except (TypeError, ValueError):
            return res
        if result.get('status', 0) != 0:
            raise BaiduException(result['status'], result['message'])
        else:
            if 'status' in result:
                result.pop('status')
            if 'message' in result:
                result.pop('message')
            if not result:
                result = True
            return result

    def get(self, url, **kwargs):
        return self._request(
            method='get',
            url=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._request(
            method='post',
            url=url,
            **kwargs
        )


class LBSClient(BaseClient):
    api_host = 'http://api.map.baidu.com'

    geodata = GeoDataAPI()
    geosearch = GeoSearchAPI()
    iplocation = IPLocationAPI()
    geoconv = GeoConvAPI()
