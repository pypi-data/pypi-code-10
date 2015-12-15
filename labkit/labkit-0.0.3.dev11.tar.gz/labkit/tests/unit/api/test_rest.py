#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.api import rest

class TestRest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_hello(self):
        return
        rest.hello()


    def test_start_server(self):
        return
        rest.start_server()


    def test_start_worker(self):
        return
        rest.start_worker()


    def test_get_password(self):
        return
        rest.get_password(username)


    def test_unauthorized(self):
        return
        rest.unauthorized()


    def test_json_get_set_name_list(self):
        return
        rest.json_get_set_name_list()


    def test_josn_get_set_list(self):
        return
        rest.josn_get_set_list(set_name)


    def test_json_get_buy_list(self):
        return
        rest.json_get_buy_list(set_name,listtype)


    def test_json_get_data_by_id(self):
        return
        rest.json_get_data_by_id(set_name,listtype,id)


    def test_json_get_data_by_id2(self):
        return
        rest.json_get_data_by_id2(id)


    def test_calc(self):
        return
        rest.calc()


    def test_pull(self):
        return
        rest.pull()


    def test_push(self):
        return
        rest.push(set_name,thing)


    def test_get_task(self):
        return
        rest.get_task(task_id)


    def test_create_task(self):
        return
        rest.create_task()


    def test_update_task(self):
        return
        rest.update_task(task_id)


    def test_delete_task(self):
        return
        rest.delete_task(task_id)


    def test_make_public_task(self):
        return
        rest.make_public_task(task)



if __name__ == '__main__':
    unittest.main()



