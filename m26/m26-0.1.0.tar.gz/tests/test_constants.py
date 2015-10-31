
import unittest

import m26


class ConstantsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_uom_miles(self):
        self.assertTrue(m26.Constants.uom_miles() == 'm', "value should be 'm'")

    def test_uom_kilometers(self):
        self.assertTrue(m26.Constants.uom_kilometers() == 'k', "value should be 'k'")

    def test_uom_yards(self):
        self.assertTrue(m26.Constants.uom_yards()== 'y', "value should be 'y'")

    def test_units_of_measure(self):
        expected = ('m', 'k', 'y')
        self.assertTrue(m26.Constants.units_of_measure()== expected, "value should be ('m', 'k', 'y')")

    def test_kilometers_per_mile(self):
        self.assertTrue(m26.Constants.kilometers_per_mile() == 1.609344, "value should be 1.609344")

    def test_miles_per_kilometer(self):
        self.assertTrue(m26.Constants.miles_per_kilometer() == 0.621371192237334, "value should be 0.621371192237334")

    def test_yards_per_kilometer(self):
        self.assertTrue(m26.Constants.yards_per_kilometer() == 1093.6132983377076, "value should be 1093.6132983377076")

    def test_feet_per_kilometer(self):
        self.assertTrue(m26.Constants.feet_per_kilometer() == 3280.839895013123, "value should be 3280.839895013123")

    def test_feet_per_meter(self):
        self.assertTrue(m26.Constants.feet_per_meter() == 3.280839895013123, "value should be 3.280839895013123")

    def test_yards_per_mile(self):
        self.assertTrue(m26.Constants.yards_per_mile() == 1760.0, "value should be 1760.0")

    def test_seconds_per_hour(self):
        self.assertTrue(m26.Constants.seconds_per_hour() == 3600.0, "value should be 3600.0")

    def test_miles_per_marathon(self):
        v = m26.Constants.miles_per_marathon()
        self.assertTrue(v == 26.2, "miles_per_marathon should be 26.2")

