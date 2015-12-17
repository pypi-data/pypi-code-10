from unittest import TestCase
from os.path import exists
from os import remove
from json import dump

decrypted_file = 'data/test.json'
encrypted_file = 'data/test_encrypted.json'


class CredkeepTestCase(TestCase):
    def setUp(self):
        self.added_files = []

    def tearDown(self):
        for fname in self.added_files:
            self.assertExists(fname)
            remove(fname)

    def add_temp(self, fname):
        """
        Add a temporary file generated from the test case

        This file *must* exist at the completion of the test or an assertion will be raised.
        :param fname: filename of temporary file
        """
        self.added_files.append(fname)

    def create_temp(self, fname, data={}):
        """
        Creates a new temporary file and registers it with the TestCase

        Created files will be cleaned up at the completion of the test

        :param fname: filename of temporary file
        :param data: Data that can be written using json.dump
        """
        self.assertNotExists(fname)
        dump(data, open(fname, 'w'))
        self.add_temp(fname)

    def assertExists(self, fname):
        """
        Asserts that a file exists
        :param fname: filename to test
        :return: The result of the assertion
        """
        return self.assertTrue(exists(fname))

    def assertNotExists(self, fname):
        """
        Asserts that a file does not already exist.
        :param fname: filename to test
        :return: The result of the assertion
        """
        return self.assertFalse(exists(fname))
