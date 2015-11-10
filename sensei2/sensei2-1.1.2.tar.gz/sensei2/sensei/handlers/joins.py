from random import choice, randint, randrange
from django.db import models
from sensei2.sensei.handlers.base import BaseHandler
from sensei2.sensei import exceptions


class JoinHandler(object):
    def set_related_qs(self, field):
        if not hasattr(self, 'related_qs'):
            setattr(self, 'related_qs', {})
        getattr(self, 'related_qs')[field.attname] = field.rel.to.objects.all()

    def prepare_value(self, obj, field, sensei):
        lst = getattr(self, 'related_qs')[field.attname]
        if len(lst) > 0:
            value = choice(lst)
            return value.pk
        else:
            return None


class ForeignKeyFieldHandler(JoinHandler, BaseHandler):
    def __init__(self):
        super(ForeignKeyFieldHandler, self).__init__()
        self.handled_class = models.ForeignKey


class OneToOneField(JoinHandler, BaseHandler):
    handled = []

    def set_related_qs(self, field):
        if not hasattr(self, 'related_qs'):
            setattr(self, 'related_qs', {})
        lst = list(field.rel.to.objects.filter(**{"%s__isnull" % field.related_query_name(): True})[:5000])
        if len(lst) < 1:
            raise exceptions.PrecacheCollection(field, self, values_count=len(lst), recomendation="Create dummy values for source one to one field")
        getattr(self, 'related_qs')[field.attname] = lst

    def __init__(self):
        super(OneToOneField, self).__init__()
        self.handled_class = models.OneToOneField

    def prepare_value(self, obj, field, sensei):
        lst = getattr(self, 'related_qs')[field.attname]
        if len(lst) > 0:
            i = randint(0, len(lst) - 1)
            value = lst[i]
            del lst[i]
            return value.pk
        else:
            return None


class M2MFieldHandler(JoinHandler, BaseHandler):
    def __init__(self):
        super(M2MFieldHandler, self).__init__()
        self.handled_class = models.ManyToManyField

    def handle(self, obj, field, sensei):
        choices_len = len(getattr(self, 'related_qs')[field.attname])
        if choices_len > 0:
            values = [choice(getattr(self, 'related_qs')[field.attname]) for x in xrange(randint(1, choices_len))]
            if not hasattr(obj, 'm2m_add_info'):
                setattr(obj, 'm2m_add_info', {})
            obj.m2m_add_info[field.attname] = set(values)
