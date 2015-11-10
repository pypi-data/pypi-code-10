# coding: utf-8
from operator import attrgetter
import string
import os
import importlib
from random import choice, randint, random
from django.db import transaction
from django.conf import settings
from django.db import models
from sensei2.sensei import helpers
from sensei2.sensei.field_handlers import BaseHandler, HandlerException
from progressbar import ProgressBar


class Sensei(object):
    def __init__(self, rule_group):
        self.rule_group = rule_group
        self.rules = getattr(settings, 'SENSEI_RULES').get(self.rule_group)
        self.paragraphs = []
        self.data = {}
        self.plugins = {}
        self.reload_files()
        self.all_handlers = [cls() for cls in helpers.get_all_subclasses(BaseHandler)]
        self.all_handlers = sorted(self.all_handlers, key=attrgetter("weight"), reverse=True)
        for plugin in getattr(settings, 'SENSEI_PLUGINS', []):
            self.init_plugin(plugin)

    @transaction.atomic
    def teach(self):
        for rule in self.rules:
            model = models.get_model(rule['app'], rule['model'])

            print "Start for %s.%s" % (rule['app'], rule['model'])
            ignore_fields = rule.get('ignore', [])
            fields = model._meta.fields + model._meta.many_to_many
            total = rule.get('total', 30)

            rule_handlers = {}  # this dict maps fields and handlers

            for field in fields:
                if field.attname not in ignore_fields:
                    # plugin has higher priority than handler
                    if 'plugins' in rule.keys() and field.attname in rule['plugins'] and rule['plugins'][
                        field.attname] in self.plugins.keys():
                        plugin = self.plugins.get(rule['plugins'][field.attname])
                        rule_handlers[field] = plugin
                    else:
                        for handler in self.all_handlers:
                            if handler.is_my_field(field):
                                handled_class = handler.get_handled_class()
                                # related qs
                                if handled_class in (models.ForeignKey, models.OneToOneField, models.ManyToManyField):
                                    handler.set_related_qs(field)
                                # overrides
                                if 'override' in rule.keys() and field.attname in rule['override']:
                                    handler.set_override_func(field, rule['override'][field.attname])
                                rule_handlers[field] = handler
                                break
                        else:
                            if not getattr(field, 'null'):
                                raise HandlerException(
                                    'no handler for field %s in model %s' % (field.attname, rule['model']))

            i = 0
            b = ProgressBar(max_value=total)
            for x in xrange(total):
                obj = model()

                for field in rule_handlers.keys():
                    handler = rule_handlers[field]
                    handler.pre_handle(obj, field, self)
                obj.clean()
                rule['presave_callback'](fields, rule, obj) if 'presave_callback' in rule.keys() else None
                obj.save()

                # handle m2m fields
                if hasattr(obj, 'm2m_add_info'):
                    m2m_add_info = getattr(obj, 'm2m_add_info')
                    for m2m_field in m2m_add_info.keys():
                        objects = m2m_add_info[m2m_field]
                        getattr(obj, m2m_field).add(*objects)
                i += 1
                b.update(i)
            print "\n"

    def reload_files(self):
        path = os.path.join(os.path.dirname(__file__), 'fill_data', 'result')
        [self.load_file(os.path.join(path, f), f[0:-4]) for f in os.listdir(path) if f[-3:] == 'txt']

    def load_file(self, file_path, to):
        self.data[to] = open(file_path).read().splitlines()

    def init_plugin(self, py_path):
        print "%s initialization..." % py_path
        self.plugins[py_path] = importlib.import_module(py_path).Plugin()

    def get_from_data(self, key):
        r = unicode(choice(self.data[key]).decode("utf-8"))
        return r if len(r) > 1 else self.get_from_data(key)

    def get_random_letter_seq(self, max_len, min_len=1):
        return ''.join(choice(string.ascii_lowercase) for x in range(randint(min_len, max_len)))

    def get_random_string(self, max_len, min_len=1):
        return ''.join(choice(string.ascii_lowercase + string.digits) for x in range(randint(min_len, max_len)))

    def get_random_int_string(self, max_len, min_len=1):
        return ''.join(choice(string.digits) for x in xrange(randint(min_len, max_len)))

    def get_random_hex_string(self):
        return ''.join(str(choice(string.digits + 'abcdef')) for x in xrange(4))

    def get_random_float(self):
        return random() * (10 ** choice([0, 1, 2, 3, 4]))

    def get_random_email(self):
        "%s@%s.%s" % (self.get_random_string(6), self.get_random_string(6), self.get_random_letter_seq(3, 2))

    def get_random_url(self):
        url = '%(protocol)s%(domain)s.%(zone)s' % {'protocol': choice(['https://', 'http://']),
                                                   'domain': self.get_random_string(10),
                                                   'zone': self.get_random_letter_seq(3)}
        if choice([0, 1]):
            pathes = [self.get_random_string(7) for x in xrange(randint(1, 5))]
            url += '/%s' % '/'.join(pathes)
        return url

    def get_random_ipv4(self):
        return '.'.join([str(randint(0, 255)) for x in xrange(4)])

    def get_random_ipv6(self):
        return ':'.join([self.get_random_hex_string() for x in xrange(8)])
