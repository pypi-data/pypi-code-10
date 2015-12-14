# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from baidu.api.base import BaseAPI


class GeoSearchAPI(BaseAPI):
    scope = 'geosearch'
    version = 'v3'

    def search_nearby(self, geotable_id, location, q='', coord_type=3,
                      radius=1000, tags=None, sortby='', filter='',
                      page_index=0, page_size=10):
        """
        poi周边搜索

        :param geotable_id: geotable主键
        :param location: 检索的中心点，逗号分隔的经纬度。样例：116.4321,38.76623
        :param q: 检索关键字。任意汉字或数字，英文字母，可以为空字符
        :param coord_type: 坐标系。3代表百度经纬度坐标系统 4代表百度墨卡托系统
        :param radius: 检索半径。单位为米，默认为1000
        :param tags: 标签。空格分隔的多字符串
        :param sortby: 排序字段。"|"分隔的多个检索条件。
                       格式为sortby={key1}:value1|{key2:val2|key3:val3}。
                       最多支持16个字段排序 {keyname}:1 升序 {keyname}:-1 降序
                       以下keyname为系统预定义的： distance 距离排序 weight 权重排序
        :param filter: 过滤条件。"|"分隔的多个key-value对。
                       key为筛选字段的名称(存储服务中定义)
                       支持连续区间或者离散区间的筛选： a:连续区间 key:value1,value2
                       b:离散区间 key:[value1,value2,value3,...]
        :param page_index: 分页索引
        :param page_size: 分页数量

        .. tips:  callback参数不支持
        """
        params = {'geotable_id': geotable_id, 'location': location}
        if q:
            params['q'] = unicode(q)
        if coord_type not in (3, 4):
            coord_type = 3
        params['coord_type'] = coord_type
        params['radius'] = radius
        if tags:
            params['tags'] = tags
        if sortby:
            params['sortby'] = sortby
        if filter:
            params['filter'] = filter
        params['page_index'] = page_index
        params['page_size'] = page_size
        return self.get('/nearby', params=params)

    def search_local(self, geotable_id, q, coord_type=3, region='', tags=None,
                     sortby='', filter='', page_index=0, page_size=10):
        """
        poi本地检索

        :param geotable_id: geotable主键
        :param q: 检索关键字。任意汉字或数字，英文字母，可以为空字符
        :param coord_type: 坐标系。3代表百度经纬度坐标系统 4代表百度墨卡托系统
        :param region: 检索区域名称。市或区的名字，如北京市，海淀区。
                       推荐填写该参数，否则，默认按照全国范围来检索
        :param tags: 标签。空格分隔的多字符串
        :param sortby: 排序字段。"|"分隔的多个检索条件。
                       格式为sortby={key1}:value1|{key2:val2|key3:val3}。
                       最多支持16个字段排序 {keyname}:1 升序 {keyname}:-1 降序
                       以下keyname为系统预定义的： distance 距离排序 weight 权重排序
        :param filter: 过滤条件。"|"分隔的多个key-value对。
                       key为筛选字段的名称(存储服务中定义)
                       支持连续区间或者离散区间的筛选： a:连续区间 key:value1,value2
                       b:离散区间 key:[value1,value2,value3,...]
        :param page_index: 分页索引
        :param page_size: 分页数量
        """
        params = {'geotable_id': geotable_id}
        if q:
            params['q'] = unicode(q)
        if coord_type not in (3, 4):
            coord_type = 3
        params['coord_type'] = coord_type
        if region:
            params['region'] = region
        if tags:
            params['tags'] = tags
        if sortby:
            params['sortby'] = sortby
        if filter:
            params['filter'] = filter
        params['page_index'] = page_index
        params['page_size'] = page_size
        return self.get('/local', params=params)

    def search_bound(self, geotable_id, bounds, coord_type=3, q='', tags=None,
                     sortby='', filter='', page_index=0, page_size=10):
        """
        poi矩形检索

        :param geotable_id: geotable主键
        :param bounds: 、矩形区域。例如：116.30,36.20;117.30,37.20
        :param coord_type: 坐标系。3代表百度经纬度坐标系统 4代表百度墨卡托系统
        :param q: 检索关键字。任意汉字或数字，英文字母，可以为空字符
        :param tags: 标签。空格分隔的多字符串
        :param sortby: 排序字段。"|"分隔的多个检索条件。
                       格式为sortby={key1}:value1|{key2:val2|key3:val3}。
                       最多支持16个字段排序 {keyname}:1 升序 {keyname}:-1 降序
                       以下keyname为系统预定义的： distance 距离排序 weight 权重排序
        :param filter: 过滤条件。"|"分隔的多个key-value对。
                       key为筛选字段的名称(存储服务中定义)
                       支持连续区间或者离散区间的筛选： a:连续区间 key:value1,value2
                       b:离散区间 key:[value1,value2,value3,...]
        :param page_index: 分页索引
        :param page_size: 分页数量
        """
        params = {'geotable_id': geotable_id, 'bounds': bounds}
        if q:
            params['q'] = unicode(q)
        if coord_type not in (3, 4):
            coord_type = 3
        params['coord_type'] = coord_type
        if tags:
            params['tags'] = tags
        if sortby:
            params['sortby'] = sortby
        if filter:
            params['filter'] = filter
        params['page_index'] = page_index
        params['page_size'] = page_size
        return self.get('/bound', params=params)

    def search_detail(self, geotable_id, uid, coord_type=3):
        """
        poi详情检索

        :param geotable_id: geotable表主键
        :param uid: uid为poi点的id值。（百度垃圾的命名，不就是记录的 ID 嘛）
        :param coord_type: 坐标系，3代表百度经纬度坐标系统 4代表百度墨卡托系统，默认3
        """
        url = '/detail/{uid}'.format(uid=uid)
        params = {
            'geotable_id': geotable_id,
            'coord_type': coord_type
        }

        result = self.get(url, params=params)
        return result['contents'][0]
