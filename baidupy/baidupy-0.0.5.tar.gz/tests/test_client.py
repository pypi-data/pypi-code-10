# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import json
import unittest
from httmock import urlmatch, HTTMock, response
from baidu.models.lbscloud import GeoTable, Column
from baidu.client import LBSClient


TESTS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURE_PATH = os.path.join(TESTS_PATH, 'fixtures')


@urlmatch(netloc=r'api\.map\.baidu\.com$')
def baidu_api_mock(url, request):
    if '/location/ip' in url.path:
        dir = 'location'
        file_name = 'ip'
    elif '/geoconv' in url.path:
        dir = 'geoconv'
        file_name = 'coords'
    else:
        dir = url.path.split('/')[1]
        file_name = '_'.join(url.path.split('/')[3:])

    res_file = os.path.join(FIXTURE_PATH, dir, '%s.json' % file_name)
    content = {
        'errcode': 99999,
        'errmsg': 'can not find fixture %s' % res_file,
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        with open(res_file, 'rb') as f:
            content = json.loads(f.read().decode('utf-8'))
    except (IOError, ValueError) as e:
        content['errmsg'] = 'Loads fixture {0} failed, error: {1}'.format(
            res_file,
            e
        )
    return response(200, content, headers, request=request)


class LBSClientTestCase(unittest.TestCase):
    ak = 'sdfgsdsfgd223wf3fwf'
    sk = 'dfgweufyg34ieifewrfegewbrvebwbe'

    def setUp(self):
        self.lbs_client = LBSClient(self.ak, self.sk)

    def test_geodata_create_geotable(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geodata.create_geotable('geotable', 1)
            self.assertTrue(result)

    def test_geodata_get_geotables(self):
        with HTTMock(baidu_api_mock):
            geotables = self.lbs_client.geodata.get_geotables()
            self.assertIsInstance(geotables, list)
            self.assertIsInstance(geotables[0], GeoTable)

    def test_geodata_get_geotable(self):
        with HTTMock(baidu_api_mock):
            geotable = self.lbs_client.geodata.get_geotable(geotable_id=23456)
            self.assertIsInstance(geotable, GeoTable)

    def test_geodata_update_geotable(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geodata.update_geotable(
                23456, name="test"
            )
            self.assertTrue(result)

    def test_geodata_delete_geotable(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geodata.delete_geotable(23456)
            self.assertTrue(result)

    def test_geodata_create_column(self):
        with HTTMock(baidu_api_mock):
            column_dict = {
                'max_length': 64,
                'default_value': '',
                'is_unique_field': False
            }
            column = Column(
                name="test",
                key="test_key",
                type=3,
                is_sortfilter_field=0,
                is_search_field=1,
                is_index_field=1,
                **column_dict
            )
            result = self.lbs_client.geodata.create_column(23456, column)
            self.assertTrue(result)

    def test_geodata_get_columns(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geodata.get_columns(23456)
            self.assertEqual(len(result), 1)
            self.assertIsInstance(result[0], Column)

    def test_geodata_get_column(self):
        with HTTMock(baidu_api_mock):
            column = self.lbs_client.geodata.get_column(23456, 345123)
            self.assertIsInstance(column, Column)

    def test_geodata_update_column(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geodata.update_column(
                23456, 345123, name="new_name"
            )
            self.assertTrue(result)

    def test_geodata_delete_column(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geodata.update_column(23456, 345123)
            self.assertTrue(result)

    def test_geosearch_search_detail(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geosearch.search_detail(23456, 1504573502)
            self.assertIsInstance(result, dict)
            self.assertEqual(result['uid'], 1504573502)

    def test_iplocation_get_location_info(self):
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.iplocation.get_location_info(
                coor='bd09ll'
            )
            self.assertIsInstance(result, dict)
            self.assertIn('point', result['content'])
            self.assertTrue(float(result['content']['point']['x']) <= 180)

    def test_geoconv_convert_coords(self):
        test_data = ("114.21892734521,29.575429778924;"
                     "114.21892734521,29.575429778924")
        test_data_list = test_data.split(';')
        with HTTMock(baidu_api_mock):
            result = self.lbs_client.geoconv.convert_coords(test_data)
            self.assertIn('result', result)
            self.assertEqual(len(result['result']), 2)
            result = self.lbs_client.geoconv.convert_coords(test_data_list)
            self.assertIn('result', result)
            self.assertEqual(len(result['result']), 2)
