from zerotest.utils import http_helper

__author__ = 'Hari Jiang'


def test_dict_to_wsgi_headers():
    data = {"blue": "yellow", "yellow": "red", "red": "blue"}
    assert sorted(http_helper.dict_to_wsgi_headers(data)) == sorted(
        [("blue", "yellow"), ("yellow", "red"), ("red", "blue")])
