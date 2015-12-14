# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from six import string_types
from collections import namedtuple
from baidu.api.base import BaseAPI
"""
----------------------------------------------------------------

----------------------------------------------------------------

gps_cor    1    GPS设备获取的角度坐标

gps_meter  2    GPS获取的米制坐标、sogou地图所用坐标;

sogou_map  3    google地图、soso地图、aliyun地图、mapabc地图和amap地图所用坐标

google_soso_aliyun_mapabc_amap    4    3中列表地图坐标对应的米制坐标
google_soso_aliyun_mapabc_amap_meter    5    百度地图采用的经纬度坐标

baidu_xy                                5    百度地图采用的经纬度坐标
baidu_meter
6：百度地图采用的米制坐标

7：mapbar地图坐标;

8：51地图坐标
"""
# 定义支持的地图坐标
_coord_type = namedtuple(
    'coord_type', ['gps_cor', 'gps_meter', 'sogou_map',
                   'google_soso_aliyun_mapabc_amap',
                   'google_soso_aliyun_mapabc_amap_meter',
                   'baidu_xy', 'baidu_meter', 'mapbar_map', 'map_51']
)
COORD_TYPE = _coord_type(
    gps_cor=1, gps_meter=2, sogou_map=2, google_soso_aliyun_mapabc_amap=3,
    google_soso_aliyun_mapabc_amap_meter=4, baidu_xy=5, baidu_meter=6,
    mapbar_map=7, map_51=8)


class GeoConvAPI(BaseAPI):
    scope = 'geoconv'
    version = 'v1'

    def convert_coords(self, coords, from_type=COORD_TYPE.gps_cor,
                       to_type=COORD_TYPE.baidu_xy):
        """
        获取 IP 对应的位置信息

        1.获取指定IP的位置信息：指定IP值，返回该IP对应的位置信息；
        2.获取当前设备IP的地址信息：根据用户设备当前的IP返回位置信息；

        :param coords: 源坐标，支持以;分隔的坐标字符串，或者可迭代坐标
        :param from_type: 源坐标类型。
        :param to_type:
        """
        if isinstance(coords, string_types):
            coords = coords.split(';')
        coords = ';'.join(coords)
        params = {}
        params['coords'] = coords
        params['from'] = from_type
        params['to'] = to_type
        params['output'] = 'json'
        return self.get('/', params=params)
