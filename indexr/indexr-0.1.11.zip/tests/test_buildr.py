#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_buildr
----------------------------------

Tests for the buildr.
"""
from indexr.buildr import *
import unittest


class TestBuildr(unittest.TestCase):
    def setUp(self):
        """
        Create some example files.
        """
        self.files = []
        self.index_path = 'index'
        if not os.path.exists(self.index_path):
            os.mkdir(self.index_path)
        with open('_test1.txt', 'w') as file:
            file.write(' Hello world.')
            self.files.append('_test1.txt')
        with open('_test2.txt', 'w') as file:
            file.write('Cool test, really!')
            self.files.append('_test2.txt')
        with open('_test3.txt', 'w') as file:
            file.write('I really really love Python')
            self.files.append('_test3.txt')
        with open('_test4.txt', 'w') as file:
            file.write('C B A')
            self.files.append('_test4.txt')

    def tearDown(self):
        """
        Remove the example files and the index.
        """
        for file in self.files:
            os.remove(file)
        shutil.rmtree(self.index_path)

    def test_indexers(self):
        """
        Test all indexers.
        """
        indexers = [BSB(show_progress=False)]
        for indexer in indexers:
            self.assertTrue(isinstance(indexer, Buildr))
            indexer.initialize(self.files, self.index_path)
            indexer.construct()
            self.assertEqual(indexer.find('Cool'), ['_test2.txt'])
            self.assertEqual(indexer.find('B'), ['_test4.txt'])
            self.assertEqual(indexer.find('really'), ['_test2.txt', '_test3.txt'])
            self.assertEqual(indexer.find('Cool', frequencies=True), {'_test2.txt': 1})
            self.assertEqual(indexer.find('really', frequencies=True), {'_test2.txt': 1, '_test3.txt': 2})


if __name__ == '__main__':
    import sys

    sys.exit(unittest.main())
