#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.api.rq_dashboard import cli

class TestCli(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_add_basic_auth(self):
        return
        cli.add_basic_auth(blueprint, username, password, realm='RQ Dashboard')


    def test_basic_http_auth(self):
        return
        cli.basic_http_auth(*args, **kwargs)


    def test_make_flask_app(self):
        return
        cli.make_flask_app(config, username, password, url_prefix)


    def test_main(self):
        return
        cli.main()



if __name__ == '__main__':
    unittest.main()



