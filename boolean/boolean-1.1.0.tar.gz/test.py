import unittest

from boolean import boolean


class BooleanTestCase(unittest.TestCase):

    def testTrue(self):
        """Test all true cases"""

        self.assertTrue(boolean('True'))
        self.assertTrue(boolean('true'))
        self.assertTrue(boolean('yes'))
        self.assertTrue(boolean('y'))
        self.assertTrue(boolean('1'))
        self.assertTrue(boolean('t'))

    def testFalse(self):
        """Test all true cases"""

        self.assertFalse(boolean('False'))
        self.assertFalse(boolean('false'))
        self.assertFalse(boolean('no'))
        self.assertFalse(boolean('n'))
        self.assertFalse(boolean('0'))
        self.assertFalse(boolean('f'))


if __name__ == '__main__':
    unittest.main()
