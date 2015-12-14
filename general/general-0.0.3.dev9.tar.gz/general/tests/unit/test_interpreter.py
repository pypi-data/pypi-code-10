#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

'''
test example contains mock and testscenarios
'''

import os
import unittest

import mock

import general.init_gs
import general.interpreter.runner as runner
from general.interpreter.runner import load_module, eval_tree, run_file

# import testscenarios

# mock.patch以及mock.patch.object只能对module对象使用, 不能直接对函数使用, 另外调用的时候也只有通过module对象调用的函数会被mock.
# mock.patch必须引用module全称, mock.patch.object可以用import进来的module别名, 此外, 修饰符只能引用全局函数,
# 因此最好用mock.patch.object + with + 类里面定义的fake函数.

# testscenarios在scenarios比较多并且完全平行的时候才有优势, 否则直接写几个函数得了.

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        # print os.path.abspath(os.path.curdir)
        # self.test_yml_file_name="general/tests/unit/proto.yml"
        self.origin_path=os.path.abspath(os.curdir)
        # os.chdir("/Users/lhr/_env/sites/91/labkit/example/")
        self.test_yml_file_name="task.yml"
        self.test_yml_file=open(self.test_yml_file_name,'r')
        # self.runner=runner

        pass

    def tearDown(self):
        self.test_yml_file.close()
        # os.chdir(self.origin_path)
        pass

    # -------- test loader ---------

    def test_is_module(self):
        '''
        test ismodule function really return a module by name
        '''
        sample_module="tests.unit.test_interpreter"
        ans=runner.load_module(sample_module)
        import inspect
        self.assertEqual(True,inspect.ismodule(ans))

        # import importlib
        # importedlib=importlib.import_module(sample_module)
        # self.assertEqual(importedlib, ans)
    def test_is_module_no_module(self):
        sample_module="gene"
        ans=runner.load_module(sample_module)
        self.assertEqual(0, ans)

    def test_load(self):
        pass
    def test_run(self):
        pass

    def test_load_module(self):
        pass
    def test_load_conf(self):
        pass

    def test_get_module_name(self):
        pass
    def test_call(self):
        pass
    def test_callrun(self):
        pass

    # --------- test runner ------------
    def eval_conf(self):
        pass

    # @staticmethod
    # def fake_run_file(self):
        # print "hello this is fake"

    def test_run_file(self):
        # with mock.patch('general.interpreter.runner.run_file',side_effect=self.fake_run_file):
        # ans=runner.run_file("ss")
        ans=runner.run_file(self.test_yml_file_name)
        pass






# class TestHelloSenario(testscenarios.TestWithScenarios):
#     scenarios=[
#         ("hello", dict(h="hello",b="1")),
#         ("world", dict(h="world",b=2))
#     ]
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def test_hello(self):
#         pass
#
#
#     def test_nother(self):
#         print self.h
#         print self.b



if __name__ == '__main__':
    unittest.main()
