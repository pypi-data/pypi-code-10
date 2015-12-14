# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from baidu.api.base import BaseAPI


class IPLocationAPI(BaseAPI):
    scope = 'location'
    version = ''

    def get_location_info(self, ip='', coor=''):
        """
        获取 IP 对应的位置信息

        1.获取指定IP的位置信息：指定IP值，返回该IP对应的位置信息；
        2.获取当前设备IP的地址信息：根据用户设备当前的IP返回位置信息；

        :param ip: ip不出现，或者出现且为空字符串的情况下，
                   会使用当前访问者的IP地址作为定位参数
        :param coor: coor不出现时，默认为百度墨卡托坐标；
                     coor="bd09ll"时，返回为百度经纬度坐标
        ..tips: coor="bd09ll"时，即其它接口中描述的 coor_type=3。
        """
        params = {}
        if ip:
            params['ip'] = ip
        if coor:
            if str(coor).lower() == 'bd09ll':
                params['coor'] = 'bd09ll'
        return self.get('/ip', params=params)
