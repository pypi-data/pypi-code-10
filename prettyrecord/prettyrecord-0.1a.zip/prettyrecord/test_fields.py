from unittest import TestCase

from prettyrecord.fields import Field, ListField, RecordField
from prettyrecord.record import Record


class TestField(TestCase):
    f1 = Field(name='_f1')
    f2 = Field(name='_f2', default_value='xxx', required=True)

    def test_init(self):
        self.assertEqual(TestField.f1.name, '_f1')
        self.assertEqual(TestField.f1.default_value, None)
        self.assertEqual(TestField.f1.required, False)

        self.assertEqual(TestField.f2.name, '_f2')
        self.assertEqual(TestField.f2.default_value, 'xxx')
        self.assertEqual(TestField.f2.required, True)

    def test_get(self):
        self.assertEqual(self.f2, TestField.f2.default_value)
        self.assertEqual(self.f2, TestField.f2.__get__(self, None))
        self.assertIs(type(TestField.f2), Field)

    def test_set(self):
        self.f2 = 5
        self.assertEqual(self.f2, 5)

    def test_del(self):
        self.f2 = 5
        del self.f2
        self.assertEqual(self.f2, 'xxx')

    def test_is_valid(self):
        self.assertTrue(TestField.f1.is_valid(None))
        self.assertFalse(TestField.f2.is_valid(None))

        self.assertTrue(TestField.f1.is_valid('xxx'))
        self.assertTrue(TestField.f1.is_valid(1.23))
        self.assertTrue(TestField.f1.is_valid([]))
        self.assertTrue(TestField.f1.is_valid(lambda: False))

    def test_normalize(self):
        with self.assertRaises(ValueError):
            TestField.f2.normalize(None)

        self.assertEqual(TestField.f2.normalize('xxx'), 'xxx')
        self.assertEqual(TestField.f2.normalize(1.23), 1.23)
        self.assertEqual(TestField.f2.normalize([]), [])
        func = lambda: False
        self.assertEqual(TestField.f2.normalize(func), func)


class TestListField(TestCase):
    def setUp(self):
        TestListField.f = ListField(lambda value: 0 <= value <= 1)

    def test_normalize(self):
        l = [0.6, 0, 1]
        self.assertSequenceEqual(TestListField.f.normalize(l), l)

        with self.assertRaises(ValueError):
            TestListField.f.normalize('abc')

        with self.assertRaises(ValueError):
            TestListField.f.normalize([1, 10, 0.5])

    def test_set_constraint(self):
        TestListField.f.constraint = lambda value: 0.4 < value < 0.6

        with self.assertRaises(ValueError):
            TestListField.f.constraint = lambda value, from_=0, to=1: from_ <= value <= to

        with self.assertRaises(TypeError):
            TestListField.f.constraint = ''


class TestRecordField(TestCase):
    class DummyRecord1(Record):
        name = Field()
        value = Field()

    class DummyRecord2(DummyRecord1):
        pass

    def setUp(self):
        TestRecordField.rf = RecordField(name='_rf', record_type=TestRecordField.DummyRecord1)

    def test_normalize(self):
        r = TestRecordField.DummyRecord1()
        self.assertIs(r, TestRecordField.rf.normalize(r))

        r = TestRecordField.DummyRecord2()
        self.assertIs(r, TestRecordField.rf.normalize(r))

        with self.assertRaises(TypeError):
            TestRecordField.rf.normalize(Record)

    def test_set_record_type(self):
        TestRecordField.rf.record_type = Record
        self.assertIs(TestRecordField.rf.record_type, Record)

        TestRecordField.rf.record_type = TestRecordField.DummyRecord2
        self.assertIs(TestRecordField.rf.record_type, TestRecordField.DummyRecord2)

        with self.assertRaises(TypeError):
            TestRecordField.rf.record_type = object