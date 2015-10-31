
import unittest

import m26


class AgeCalculatorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_seconds_per_year(self):
        self.assertTrue(m26.AgeCalculator.seconds_per_year() == 31557600.0, "value should be 31557600.0")

    def test_milliseconds_per_year(self):
        self.assertTrue(m26.AgeCalculator.milliseconds_per_year() == 31557600000.0, "value should be 31557600000.0")

    def test_calculate(self):
        a1 = m26.AgeCalculator.calculate('1960-10-01', '2015-10-01')
        actual = 54.997946611909654
        self.assertTrue(a1.value > (actual - 0.000001), "value is too small")
        self.assertTrue(a1.value < (actual + 0.000001), "value is too large")
