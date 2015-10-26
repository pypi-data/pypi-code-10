from unittest import TestCase

from prettyrecord.name_utils import mangle_name, unmangle_name, get_object


class TestNameUtils(TestCase):
    class Dummy:
        x = 10

    def test_mangle_name(self):
        self.assertEqual(mangle_name(TestNameUtils.Dummy, 'x'), '_Dummy__x')
        self.assertEqual(mangle_name('Dummy', 'x'), '_Dummy__x')

    def test_unmangle_name(self):
        self.assertEqual(unmangle_name('_Dummy__x'), 'x')
        self.assertEqual(unmangle_name('x'), 'x')

    def test_get_object(self):
        self.assertIs(TestNameUtils.Dummy, get_object('TestNameUtils.Dummy'))

        with self.assertRaises(NameError):
            get_object('TestNameUtils.Dummy2')

        with self.assertRaises(NameError):
            get_object('TestUtilitiEs.Dummy')

        class NestedDummy:
            class MoreNestedDummy1:
                pass

            class MoreNestedDummy2:
                sth = get_object("TestNameUtils.test_get_object.<locals>.NestedDummy.MoreNestedDummy1")

        self.assertIs(NestedDummy.MoreNestedDummy2.sth, NestedDummy.MoreNestedDummy1)