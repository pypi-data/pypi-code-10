from zope.interface import implements
from copy import deepcopy

from rapido.core.interfaces import IRecordable

from .interfaces import IRecord


class Record(object):
    implements(IRecord, IRecordable)

    def __init__(self, context, app):
        self.context = context
        self.app = app

    def set_item(self, name, value):
        """ set an item value
        """
        self.context.attrs[name] = value

    def get_item(self, name):
        """ return an item value
        """
        if(self.has_item(name)):
            return deepcopy(self.context.attrs[name])

    def has_item(self, name):
        """ test if item exists
        """
        return name in self.context.attrs

    def remove_item(self, name):
        """ remove an item
        """
        if name in self.context.attrs:
            del self.context.attrs[name]

    def uid(self):
        """ return internal identifier
        """
        return self.context.intid

    def items(self):
        """ return all items
        """
        return dict(self.context.attrs)
