import unittest

class encodingTest(unittest.TestCase):
    def test_bin(self):
        b = "asd".encode("bin")
        self.assertEqual("asd", b.decode("bin"))

        a = "01100001011100110110010".decode("bin")
        self.assertEqual("as",a)
