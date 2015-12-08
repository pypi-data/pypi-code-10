# -*- coding: utf-8 -*
from __future__ import unicode_literals, print_function

import os
import shutil
import unittest

from crotal.site import Site
from base import BaseTest


SITE_MAP = [
    u'preview/tags/computer science/index.html',
    u'preview/tags/python/index.html',
    u'preview/about/index.html',
    u'preview/question-of-life-universe-everything/index.html',
    u'preview/archives/index.html',
    u'preview/categories/math/index.html',
    u'preview/page/2/index.html',
    u'preview/categories/others/index.html',
    u'preview/csapp/index.html',
    u'preview/tags/jersey devil/index.html',
    u'preview/tags/csapp/index.html',
    u'preview/archives/2013/11/index.html',
    u'preview/archives/2014/11/index.html',
    u'preview/robots.txt',
    u'preview/tags/monty hall/index.html',
    u'preview/categories/people/index.html',
    u'preview/monty-hall-problem/index.html',
    u'preview/about/cinema/index.html',
    u'preview/tags/larry wall/index.html',
    u'preview/categories/tutorial/index.html',
    u'preview/archives/2014/10/index.html',
    u'preview/make-some-sketches/index.html',
    u'preview/archives/2015/10/index.html',
    u'preview/larry-wall/index.html',
    u'preview/categories/book/index.html',
    u'preview/tags/jersey legends/index.html',
    u'preview/index.html',
    u'preview/tags/book/index.html',
    u'preview/archives/2012/10/index.html',
    u'preview/python-in-a-nutshell/index.html',
    u'preview/categories/web/index.html',
    u'preview/jersey-devil/index.html',
    u'preview/archives/2013/10/index.html',
    u'preview/rss.xml',
]


class TestSite(BaseTest):

    def setUp(self):
        self.site_path = os.path.join(self.data_dir, 'test_site')
        self.output_path = os.path.join(self.site_path, 'preview')
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        shutil.rmtree(self.output_path)

    def test_site_generate_full(self):
        self.generate_site(full=True)
        file_list_after_generate = self.scan_files(self.output_path)
        self.assertSetEqual(set(SITE_MAP), set(file_list_after_generate))

    def test_site_generate(self):
        self.generate_site()
        file_list_after_generate = self.scan_files(self.output_path)
        self.assertSetEqual(set(SITE_MAP), set(file_list_after_generate))

    def generate_site(self, full=False):
        site = Site(self.site_path, full=full)
        site.generate()

    def scan_files(self, absolute_path):
        """
        This method returns the list of all the source files in the directory
        indicated. Notice that file started with '.' will not be
        included.
        """
        file_list = []
        for dir_, _, files in os.walk(absolute_path):
            for file_name in files:
                absolute_file = os.path.join(dir_, file_name)
                if not file_name.startswith('.'):
                    file_path = os.path.relpath(absolute_file, self.site_path)
                    file_list.append(file_path)
        return file_list

if __name__ == '__main__':
    unittest.main()
