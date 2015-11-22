import corto
import unittest

class Test(unittest.TestCase):

    def setUp(self):
        corto.start()

    def tearDown(self):
        corto.stop()

    def test_start_stop(self):
        pass

    def test_corto_o(self):
        corto_o = corto.resolve(None, "corto")
