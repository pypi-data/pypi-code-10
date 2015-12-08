# coding=utf8
from __future__ import unicode_literals

import json
import os
import unittest

import requests

from tests.helper.process import call_process
from tests.mock.mock_server import Server
from tests.mock.zerotest_proxy import Proxy
from zerotest.utils.url_helper import urljoin

server = None
proxy = None
zerotest_cmd = "python zerotest/cli.py"


def init_test_env():
    global server, proxy
    try:
        server = Server()
        server.start_mock_server()
        proxy = Proxy()
        proxy.start_server(server.url)
    except:
        destroy_test_env()
        raise


def destroy_test_env():
    global server, proxy
    if proxy:
        proxy.shutdown()
    if server:
        server.shutdown()


class TestZerotest(unittest.TestCase):
    def setUp(self):
        init_test_env()

    def tearDown(self):
        destroy_test_env()
        if proxy.data_file:
            os.remove(proxy.data_file)

    def test_proxy(self):
        # test 404
        res = requests.get(urljoin(proxy.url, 'echo'))
        assert res.status_code == 404

        res = requests.post(urljoin(server.url, 'echo'), data='who am I?')
        res.raise_for_status()
        assert res.text == 'who am I?'

        res = requests.post(urljoin(proxy.url, 'echo'), data='who am I?')
        res.raise_for_status()
        assert res.text == 'who am I?'

        res = requests.post(urljoin(proxy.url, 'echo'), data=json.dumps({"say": "hello", "name": "tester"}),
                            headers={"Content-Type": "application/json; charset=utf-8"})
        res.raise_for_status()
        assert res.json() == {"say": "hello", "name": "tester"}

        res = requests.get(urljoin(proxy.url, 'count'))
        res.raise_for_status()
        assert isinstance(res.json()['count'], int)

        data = dict(name="test json convert", magic_number=7)
        res = requests.post(urljoin(proxy.url, 'raw/to.json'), data=json.dumps(data))
        res.raise_for_status()
        assert data == res.json()

        res = requests.get(urljoin(proxy.url, 'chinese/hello-world'))
        res.raise_for_status()
        assert res.json()['content'] == '你好,世界'
        proxy.shutdown()

    def test_replay(self):
        # test replay
        replay = lambda args: call_process(zerotest_cmd + args + " -t='-vv'")
        assert replay(" replay not_exist_file") != 0
        assert replay(" replay {}".format(proxy.data_file)) != 0
        assert replay(" replay {} --ignore-all-headers".format(proxy.data_file)) != 0
        assert replay(" replay {} --ignore-all-headers --ignore-fields count".format(proxy.data_file)) == 0
        assert replay(" replay {} --ignore-headers date --ignore-fields count".format(proxy.data_file)) == 0
        assert replay(" replay {} --ignore-headers date --fuzzy".format(proxy.data_file)) == 0
