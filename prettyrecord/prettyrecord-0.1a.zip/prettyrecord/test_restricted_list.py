from unittest import TestCase

from prettyrecord.restricted_list import RestrictedList


class TestRestrictedList(TestCase):
    def setUp(self):
        self.constraint = lambda value: 1 <= value <= 10
        self.data_source = [1, 2, 3]
        self.list = RestrictedList(constraint=self.constraint, source=self.data_source)

    def test_init(self):
        self.list = RestrictedList(constraint=self.constraint, source=[1, 5, 10])

        with self.assertRaises(ValueError):
            self.list = RestrictedList(constraint=self.constraint, source=[1, 20, 10])

    def test_setitem(self):
        self.list[0] = 9
        self.assertEqual(self.list[0], 9)

        with self.assertRaises(ValueError):
            self.list[0] = 11

    def test_eq(self):
        self.assertEqual(self.list, self.data_source)
        self.assertEqual(self.list, RestrictedList(constraint=lambda value: True, source=self.data_source))
        self.assertNotEqual(self.list, [1, 100, 500])

    def test_insert(self):
        self.list.insert(0, 1)
        self.list.insert(1, 10)

        with self.assertRaises(ValueError):
            self.list.insert(1, 11)

    def test_is_valid(self):
        self.assertTrue(self.list.is_valid(1))
        self.assertTrue(self.list.is_valid(5))
        self.assertTrue(self.list.is_valid(10))
        self.assertFalse(self.list.is_valid(None))
        self.assertFalse(self.list.is_valid('1'))