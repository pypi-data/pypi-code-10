# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from baidu import exceptions
from baidu.models import empty
from baidu.models.lbscloud import Column, GeoTable
from baidu.api.base import BaseAPI


class GeoDataAPI(BaseAPI):
    """
    """
    scope = 'geodata'
    version = 'v3'

    def create_geotable(self, name, is_published, geotype=1):
        """
        创建表（create geotable）接口

        :param name: geotable的中文名称
        :param is_published: 是否发布到检索
        :param geotype: geotable持有数据的类型。1：点；2：线；3：面。默认为1（当前只支持点）
        """
        # 目前只支持点
        if geotype != 1:
            geotype = 1
        data = {
            'name': name,
            'geotype': geotype,
            'is_published': is_published
        }
        result = self.post('/geotable/create', data=data)
        return result['id'] > 0

    def get_geotables(self, name=empty):
        """
        查询表（list geotable）接口

        :param name: geotable的名字
        """
        if name is empty or not name:
            params = {}
        else:
            params = {'name': name}
        result = self.get('/geotable/list', params=params)
        geotables = []
        if result['size'] > 0:
            for geotable_info in result['geotables']:
                geotables.append(GeoTable(**geotable_info))

        return geotables

    def get_geotable_by_name(self, geotable_name):
        """
        通过位置数据表的表名获取表对象

        .. tips:
            此方法不是百度 LSB API支持的，而是从`get_geotables`变形而来。
        """
        geotables = self.get_geotables(name=geotable_name)
        if len(geotables) == 0:
            raise exceptions.GeotableDoesNotExistException()
        assert len(geotables) == 1, "位置数据表的名称不唯一"
        return geotables[0]

    def get_geotable(self, geotable_id):
        """
        查询指定id表（detail geotable）接口

        :param geotable_id: 指定geotable的id
        """
        result = self.get('/geotable/detail', params={'id': geotable_id})
        assert 'geotable' in result
        return GeoTable(**result['geotable'])

    def update_geotable(self, geotable_id, name=empty, is_published=empty):
        """
        修改表（update geotable）接口

        :param geotable_id: geotable主键
        :param name: geotable的中文名称
        :param is_published: 是否发布到检索(会引起批量操作)
        """
        data = {'id': geotable_id}
        if name not in (empty, None):
            data['name'] = name
        if is_published not in (empty, None):
            data['is_published'] = is_published

        return self.post('/geotable/update', data=data)

    def delete_geotable(self, geotable_id):
        """
        删除表（geotable）接口

        :param geotable_id: 指定geotable的id

        注意： 当geotable里面没有有效数据时，才能删除geotable。
        """
        return self.post('/geotable/delete', data={'id': geotable_id})

    def create_column(self, geotable_id, column):
        """
        创建列（create column）接口

        :param geotable_id: 所属于的geotable_id
        :param column: 列定义
        """
        assert isinstance(column, Column)
        data = {'geotable_id': geotable_id}
        data.update(column.data)
        if 'id' in data:
            data.pop('id')
        result = self.post('/column/create', data=data)
        return result['id'] > 0

    def get_columns(self, geotable_id, name=None, key=None):
        """
        查询列（list column）接口

        :param geotable_id: 所属于的geotable_id
        :param name: geotable meta的属性中文名称
        :param key: geotable meta存储的属性key
        """
        params = {'geotable_id': geotable_id}
        if name is not empty and name:
            params['name'] = name
        if key is not empty and key:
            params['key'] = key
        result = self.get('/column/list', params=params)
        column_list = []
        if result['size'] > 0:
            for column_info in result['columns']:
                column_list.append(Column(**column_info))
        return column_list

    def get_column(self, geotable_id, column_id):
        """
        查询指定id列（detail column）详情接口

        :param geotable_id: 所属于的geotable_id
        :param column_id: 列的id

        """
        params = {'geotable_id': geotable_id, 'id': column_id}
        result = self.get('/column/detail', params=params)
        return Column(**result['column'])

    def update_column(self, geotable_id, column_id, **kwargs):
        """
        修改指定条件列（column）接口

        :param geotable_id: 所属于的geotable_id
        :param column_id: 列的id

        :param name: 属性中文名称，可选
        :param default_value: 默认值，可选
        :param max_length: 文本最大长度，可选
        :param is_sortfilter_field: 是否检索引擎的数值排序字段，可选
        :param is_search_field: 是否检索引擎的文本检索字段，可选
        :param is_index_field: 是否存储引擎的索引字段，可选
        :param is_unique_field: 是否存储索引的唯一索引字段，可选
        """
        optionals = (
            'name', 'default_value', 'max_length', 'is_sortfilter_field',
            'is_search_field', 'is_index_field', 'is_unique_field'
        )
        data = {'geotable_id': geotable_id, 'id': column_id}
        for key in kwargs:
            if key not in optionals:
                kwargs.pop(key)
            if 'key' in kwargs and kwargs['key'] is empty:
                kwargs.pop(key)
        data.update(kwargs)
        return self.post('/column/update', data=data)

    def delete_column(self, geotable_id, column_id):
        """
        删除指定条件列（column）接口

        :param geotable_id: 所属于的geotable_id
        :param column_id: 列的id
        """
        data = {'geotable_id': geotable_id, 'id': column_id}
        return self.post('/column/delete', data=data)

    def create_poi(
            self,
            geotable_id,
            longitude,
            latitude,
            coord_type,
            **kwargs):
        """
        创建数据（create poi）接口

        TODO: 用户在column定义的key/value对？

        :param geotable_id: 记录关联的geotable的标识
        :param longitude: 用户上传的经度
        :param latitude: 用户上传的纬度
        :param coord_type: 用户上传的坐标的类型
        :param title: poi名称，可选
        :param address: 地址，可选
        :param tags: tags，可选
        """
        data = {
            'geotable_id': geotable_id,
            'latitude': latitude,
            'longitude': longitude,
            'coord_type': coord_type,
        }
        data.update(kwargs)
        result = self.post('/poi/create', data=data)
        return result['id']

    def get_pois(self, geotable_id, page_index=0, page_size=10, **kwargs):
        """
        查询指定条件的数据（poi）列表接口

        column需要设置了is_index_field=1。对于string，是两端匹配。对于int或者double，则是范围查找，传递的格式为最小值,最大值。当无最小值或者最大值时，用-代替，同时，此字段最大长度不超过50，最小值与最大值都是整数
        例：如加入一个命名为color数据类型为string的column，在检索是可设置为“color=red”的形式来检索color字段为red的POI

        :param geotable_id: 记录关联的geotable的标识
        :param title: 记录（数据）名称
        :param tags: 记录的标签（用于检索筛选）
        :param bounds: 查询的矩形区域
        :param page_index: 分页索引
        :param page_size: 分页数目

        """

        params = {'geotable_id': geotable_id}
        params.update(kwargs)
        return self.get('/poi/list', params=params)

    def get_poi(self, geotable_id, poi_id):
        """
        查询指定id的数据（poi）详情接口

        :param poi_id: 表主键
        :param geotable_id: poi主键

        """
        params = {'geotable_id': geotable_id, 'id': poi_id}
        return self.get('/poi/detail', params=params)

    def update_poi(self, geotable_id, poi_id, coord_type=3, **kwargs):
        """
        修改数据（poi）接口

        :param geotable_id: 记录关联的geotable的标识
        :param poi_id: poi的id
        :param coord_type: 用户上传的坐标的类型
        """

        data = {
            'geotable_id': geotable_id,
            'id': poi_id,
            'coord_type': coord_type
        }
        data.update(kwargs)
        result = self.post('/poi/update', data=data)
        return result['id'] == poi_id

    def delete_poi(
            self,
            geotable_id,
            poi_id=empty,
            poi_ids=empty,
            is_total_del=empty,
            **kwargs
            ):
        """
        删除数据（poi）接口（支持批量）

        :param geotable_id: geotable_id
        :param poi_id: 如果传了这个参数，此其它的删除条件会被忽略，此时此操作不是批量请求。只会最多删除一个poi
        :param poi_ids: 最多1000个id,如果有这个条件,其它条件将被忽略.
        :param title: 名称
        :param tags: 标签
        :param bounds: string 查询的矩形区域， 格式x1,y1;x2,y2分别代表矩形的左上角和右下角

        """
        data = {
            'geotable_id': geotable_id,
        }
        if poi_id is not empty:
            data['id'] = poi_id
        elif poi_ids is not empty and isinstance(poi_ids, list):
            data['ids'] = ','.join(poi_ids)
        else:
            data.update(kwargs)

        # 如果是批量删除，则需要传这个参数，值为1；如果不是批量删除，则不用传这个参数
        if is_total_del == 1:
            data['is_total_del'] = 1
        self.post('/poi/delete', data=data)
        return True

    # def upload_poi(self,):
    #     """
    #
    #     """
