from random import randint
from termcolor import colored, cprint
import inspect


class HandlerException(Exception):
    def __init__(self, message):
        self.message = message


class BaseHandler(object):
    def __init__(self):
        self.overrides = {}

    @property
    def weight(self):
        return len(inspect.getmro(self.get_handled_class()))

    def is_my_field(self, field):
        return isinstance(field, self.get_handled_class())

    def get_handled_class(self):
        return self.handled_class

    def set_override_func(self, field, override_func):
        self.overrides[field.attname] = override_func

    def pre_handle(self, obj, field, sensei):
        # execute or not handler for nullable fields
        if getattr(field, 'null', False) is True and randint(0, 1) == 1:
            return
        return self.handle(obj, field, sensei)

    def handle(self, obj, field, sensei):
        if hasattr(self, 'object_mode'):
            self.object_mode(obj, field, sensei)
            return

        if field.attname in self.overrides:
            value = self.overrides[field.attname](obj, field, sensei)
        else:
            value = self.prepare_value(obj, field, sensei)

        try:
            field.validate(value, obj)
        except Exception, e:
            print cprint("Invalid value %s for field <b>%s. Django error:%s" % (value, field.attname, str(e)), "red")
            raise e

        setattr(obj, field.attname, value)

    def prepare_value(self, obj, field, sensei):
        raise NotImplemented
