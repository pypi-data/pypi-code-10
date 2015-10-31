
import unittest

import m26


class DistanceTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_constructor_miles(self):
        d = m26.Distance()
        self.assertTrue(d.value == 0,  "value should be 0")
        self.assertTrue(d.uom  == 'm', "uom should be 'm'")

        d = m26.Distance(26.2)
        self.assertTrue(d.value == 26.2, "value should be 26.2")
        self.assertTrue(d.uom  == 'm', "uom should be 'm'")

        self.assertTrue(d.is_miles(),       "is_miles should be true")
        self.assertFalse(d.is_kilometers(), "is_kilometers should be false")
        self.assertFalse(d.is_yards(),      "is_yards should be false")

        self.assertAlmostEqual(d.as_miles(),      26.2)
        self.assertAlmostEqual(d.as_kilometers(), 42.1648128)
        self.assertAlmostEqual(d.as_yards(),      46112.0)

    def test_constructor_kilometers(self):
        d = m26.Distance(50.0, 'k')
        self.assertTrue(d.value == 50.0, "value should be 50.0")
        self.assertTrue(d.uom  == 'k', "uom should be 'k'")

        d = m26.Distance(10, ' K ')
        self.assertTrue(d.value == 10.0, "value should be 10.0")
        self.assertTrue(d.uom  == 'k', "uom should be 'k'")

        self.assertFalse(d.is_miles(),     "is_miles should be false")
        self.assertTrue(d.is_kilometers(), "is_kilometers should be true")
        self.assertFalse(d.is_yards(),     "is_yards should be false")

        self.assertAlmostEqual(d.as_miles(),      6.2137119223733395)
        self.assertAlmostEqual(d.as_kilometers(), 10.000000)
        self.assertAlmostEqual(d.as_yards(),      10936.132983377078)

    def test_constructor_yards(self):
        d = m26.Distance(3600.0, 'y')
        self.assertTrue(d.value == 3600.0, "value should be 3600.0")
        self.assertTrue(d.uom == 'y', "uom should be 'y'")

        d = m26.Distance(1800.0, ' Y ')
        self.assertTrue(d.value == 1800.0, "value should be 1800.0")
        self.assertTrue(d.uom == 'y', "uom should be 'y'")

        self.assertFalse(d.is_miles(),      "is_miles should be false")
        self.assertFalse(d.is_kilometers(), "is_kilometers should be false")
        self.assertTrue(d.is_yards(),       "is_yards should be true")

        self.assertAlmostEqual(d.as_miles(),      1.0227272727272727)
        self.assertAlmostEqual(d.as_kilometers(), 1.64592)
        self.assertAlmostEqual(d.as_yards(),      1800.000000)

    def test_add(self):
        d1 = m26.Distance(26.2, 'm')
        d2 = m26.Distance(4.8, 'm')
        d3 = m26.Distance(5.0, 'k')
        d4 = m26.Distance(1800, 'y')

        d1.add(d2)
        self.assertAlmostEqual(d1.value, 31.0)
        self.assertTrue(d1.uom == 'm', "uom should be 'm'")

        d1.add(d3)
        self.assertAlmostEqual(d1.value, 34.10685596118667)

        d1.add(d4)
        self.assertAlmostEqual(d1.value, 35.12958323391394)
        self.assertTrue(d1.uom == 'm', "uom should be 'm'")

    def test_subtract(self):
        d1 = m26.Distance(26.2, 'm')
        d2 = m26.Distance(4.8, 'm')
        d3 = m26.Distance(5.0, 'k')
        d4 = m26.Distance(1800, 'y')

        d1.subtract(d2)
        self.assertAlmostEqual(d1.value, 21.4)
        self.assertTrue(d1.uom == 'm', "uom should be 'm'")

        d1.subtract(d3)
        self.assertAlmostEqual(d1.value, 18.293144038813328)

        d1.subtract(d4)
        self.assertAlmostEqual(d1.value, 17.270416766086054)
        self.assertTrue(d1.uom == 'm', "uom should be 'm'")
