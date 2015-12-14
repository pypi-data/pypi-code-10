#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


import unittest

from labkit.cmd import cli

class TestCli(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_push(self):
        return
        cli.push(yml_file='task.yml')


    def test_runner(self):
        return
        cli.runner(yml_file='task.yml')


    def test_worker(self):
        return
        cli.worker(queue_names='compute')


    def test_front(self):
        return
        cli.front(queue_names='tasks')


    def test_rest(self):
        return
        cli.rest()


    def test_start(self):
        return
        cli.start()


    def test_startdb(self):
        return
        cli.startdb()


    def test_backup(self):
        return
        cli.backup()


    def test_restore(self):
        return
        cli.restore()


    def test_cli(self):
        return
        cli.cli()



if __name__ == '__main__':
    unittest.main()



