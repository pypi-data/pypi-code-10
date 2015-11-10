from decimal import *
from random import randint, choice
from django.db import models
from sensei2.sensei.handlers.base import BaseHandler


class IntegerFieldHandler(BaseHandler):
    def __init__(self):
        super(IntegerFieldHandler, self).__init__()
        self.handled_class = models.IntegerField

    def prepare_value(self, obj, field, sensei):
        return randint(-9999, 9999) if not field.choices else choice([x[0] for x in field.choices])


class PositiveIntegerFieldHandler(BaseHandler):
    priority = 1

    def __init__(self):
        super(PositiveIntegerFieldHandler, self).__init__()
        self.handled_class = models.PositiveIntegerField

    def prepare_value(self, obj, field, sensei):
        return randint(0, 9999) if not field.choices else choice([x[0] for x in field.choices])


class SmallIntegerFieldHandler(BaseHandler):
    priority = 1

    def __init__(self):
        super(SmallIntegerFieldHandler, self).__init__()
        self.handled_class = models.SmallIntegerField

    def prepare_value(self, obj, field, sensei):
        return randint(-999, 999) if not field.choices else choice([x[0] for x in field.choices])


class PositiveSmallIntegerFieldHandler(BaseHandler):
    priority = 2

    def __init__(self):
        super(PositiveSmallIntegerFieldHandler, self).__init__()
        self.handled_class = models.PositiveSmallIntegerField

    def prepare_value(self, obj, field, sensei):
        return randint(0, 999) if not field.choices else choice([x[0] for x in field.choices])


class FloatFieldHandler(BaseHandler):
    def __init__(self):
        super(FloatFieldHandler, self).__init__()
        self.handled_class = models.FloatField

    def prepare_value(self, obj, field, sensei):
        return sensei.get_random_float() if not field.choices else choice([x[0] for x in field.choices])


class BooleanFieldHandler(BaseHandler):  # need test
    def __init__(self):
        super(BooleanFieldHandler, self).__init__()
        self.handled_class = models.BooleanField

    def prepare_value(self, obj, field, sensei):
        return bool(randint(0, 1))


class NullBooleanFieldHandler(BaseHandler):
    def __init__(self):
        super(NullBooleanFieldHandler, self).__init__()
        self.handled_class = models.NullBooleanField

    def prepare_value(self, obj, field, sensei):
        return choice([bool(1), bool(0), None])


class AutoFieldHandler(BaseHandler):
    def __init__(self):
        super(AutoFieldHandler, self).__init__()
        self.handled_class = models.AutoField

    def pre_handle(self, obj, field, sensei):
        pass


class BigIntegerFieldHandler(BaseHandler):
    priority = 1

    def __init__(self):
        super(BigIntegerFieldHandler, self).__init__()
        self.handled_class = models.BigIntegerField

    def prepare_value(self, obj, field, sensei):
        return randint(-9223372036854775808, 9223372036854775807)


class CommaSeparatedIntegerFieldHandler(BaseHandler):
    priority = 1

    def __init__(self):
        super(CommaSeparatedIntegerFieldHandler, self).__init__()
        self.handled_class = models.CommaSeparatedIntegerField

    def prepare_value(self, obj, field, sensei):
        max_number_len = (getattr(field, 'max_length') - 1) / 2
        return '%(part1)s,%(part2)s' % {'part1': sensei.get_random_int_string(max_len=max_number_len),
                                        'part2': sensei.get_random_int_string(max_len=max_number_len)}


class DecimalFieldHandler(BaseHandler):
    def __init__(self):
        super(DecimalFieldHandler, self).__init__()
        self.handled_class = models.DecimalField

    def prepare_value(self, obj, field, sensei):
        max_digits = getattr(field, 'max_digits')
        decimal_places = getattr(field, 'decimal_places')
        value = '%(part1)s.%(part2)s' % {'part1': sensei.get_random_int_string(max_len=max_digits - decimal_places),
                                         'part2': sensei.get_random_int_string(max_len=decimal_places)}
        return Decimal(value)
