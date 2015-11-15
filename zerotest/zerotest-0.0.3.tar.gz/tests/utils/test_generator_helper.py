from collections import OrderedDict

from zerotest.request import Request
from zerotest.utils.generator_helper import get_name_from_request, dict_to_param_style_code

__author__ = 'Hari Jiang'


def test_get_name_from_request():
    req = Request(path='/', method='GET')
    assert get_name_from_request(req) == 'get_root'
    req = Request(path='/the/world', method='PUT')
    assert get_name_from_request(req) == 'put_the_world'


def test_dict_to_param_style_code():
    test_dict = OrderedDict()
    test_dict['param_a'] = 'A'
    test_dict['test_c'] = 'C'
    assert dict_to_param_style_code(test_dict) == "param_a='A', test_c='C'"
