# coding=utf-8
from __future__ import print_function
from unittest import TestCase

from flyforms.core import Field
from flyforms.fields import *
from flyforms.validators import ValidationError
from flyforms.common import UNSET


# noinspection PyUnresolvedReferences
class MixinTestField(object):
    field_cls = Field
    valid_values = []
    invalid_values = []

    def test(self):
        field = self.field_cls()
        for vv in self.valid_values:
            field.validate(vv)
        for iv in self.invalid_values:
            with self.assertRaises(ValidationError):
                field.validate(iv)


class TestStringField(TestCase, MixinTestField):
    field_cls = StringField
    valid_values = ["", " ", u" ", u"qwerty", "Hello world!"]
    invalid_values = [None, object(), 0.25, 15, UNSET]

    def test_regex(self):
        field = self.field_cls(regex=r"^[A-Z].*$")
        self.check(field)

    def test_validators_add(self):
        from flyforms.validators import RegexValidator
        field = self.field_cls(
            min_length=1,
            max_length=10,
            validators=(RegexValidator(regex=r"^[A-Z].*$"),))
        self.check(field)

    def check(self, field):
        for vv in ["A__", "W", "WWW"]:
            field.validate(vv)
        for iv in ["_AAA", "", "aaa"]:
            with self.assertRaises(ValidationError):
                field.validate(iv)


class TestEmailField(TestCase, MixinTestField):
    field_cls = EmailField
    valid_values = ["qwerty@gmail.com", "John@Smith.ua"]
    invalid_values = [None, UNSET, "@gmail.com", "qwerty@gmail,com", "qwerty_gmail.com"]


class TestIntField(TestCase, MixinTestField):
    field_cls = IntField
    valid_values = [0, 10, -50]
    invalid_values = [0.1, object(), UNSET]


class TestFloatField(TestCase, MixinTestField):
    field_cls = FloatField
    valid_values = [0.0, 10.1, -100500.0]
    invalid_values = [0, UNSET, object()]

    def test_attrs(self):
        with self.assertRaises(ValidationError):
            FloatField(min_value=0.0).validate(-0.05)


class TestIp4Field(TestCase, MixinTestField):
    field_cls = Ip4Field
    valid_values = ["127.0.0.1", "192.188.1.1"]
    invalid_values = [UNSET, "1270.0.1", "192.1881.1", None, object()]


class TestBoolField(TestCase, MixinTestField):

    class BClass(object):
        def __nonzero__(self):
            return False

    field_cls = BooleanField
    valid_values = [True, False]
    invalid_values = [0, UNSET, 100500.2, BClass()]
