import os
import os.path
import tempfile
import unittest


class TestManager(unittest.TestCase):
    fh = None
    path = ''

    def setUp(self):
        os.makedirs('finddata')
        self.fh, self.path = tempfile.mkstemp(dir='finddata')

    def tearDown(self):
        os.remove(self.path)
        os.removedirs('finddata')

    def test_find_package(self):
        from sergelab.utils.setup import find_package_data
        self.assertEqual(find_package_data('finddata'), {'finddata': [os.path.basename(self.path)]})

    def test_test_and_install(self):
        from sergelab.utils.setup import test_and_install

    def test_clean(self):
        from sergelab.utils.setup import clean
