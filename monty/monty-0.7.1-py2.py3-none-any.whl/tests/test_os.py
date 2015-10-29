__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os

from monty.os.path import which, zpath
from monty.os import cd, makedirs_p

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

class PathTest(unittest.TestCase):

    def test_which(self):
        py = which("python")
        self.assertEqual(os.path.basename(py), "python")

    def test_zpath(self):
        fullzpath = zpath(os.path.join(test_dir, "myfile_gz"))
        self.assertEqual(os.path.join(test_dir, "myfile_gz.gz"), fullzpath)


class CdTest(unittest.TestCase):

    def test_cd(self):
        with cd(test_dir):
            self.assertTrue(os.path.exists("empty_file.txt"))
        self.assertFalse(os.path.exists("empty_file.txt"))

    def test_cd_exception(self):
        try:
            with cd(test_dir):
                self.assertTrue(os.path.exists("empty_file.txt"))
                raise RuntimeError()
        except:
            pass
        self.assertFalse(os.path.exists("empty_file.txt"))


class Makedirs_pTest(unittest.TestCase):

    def setUp(self):
        self.test_dir_path = os.path.join(test_dir, "test_dir")

    def test_makedirs_p(self):
        makedirs_p(self.test_dir_path)
        self.assertTrue(os.path.exists(self.test_dir_path))
        makedirs_p(self.test_dir_path)
        self.assertRaises(OSError, makedirs_p, os.path.join(test_dir, "myfile_txt"))

    def tearDown(self):
        os.rmdir(self.test_dir_path)


if __name__ == "__main__":
    unittest.main()
