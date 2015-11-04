# -*- encoding: utf-8 -*-
import six
import logging

from any2 import TypeTransformer
from any2 import recursive_getattr
from any2 import ColumnMappingError

log = logging.getLogger(__name__)


class BaseAdapter(object):
    """New style adapter that adapts an iterator to another one
    This is the base class and should be used for all your new style adapters
    """
    def __init__(self, iterator, transformer=None):
        """the base constructor for all our adapters.

        :param iterator: the iterator to adapt.
        :param transformer: an optional any2.transformers.BaseTransformer
        :return: an adapted iterator, the exact properties of this new iterator
        depends on the implementer
        """
        self.iterator = iterator
        if not transformer:
            transformer = TypeTransformer()

        self.transformer = transformer


class Listlike2List(BaseAdapter):
    """an adapter that takes an iterator yielding list like objects and gives
    a new iterator that yields real lists containing the same number of items
    but potentially transformed using the transformer you gave to its
    constructor. Transformers are available in any2.transformers
    """

    def __iter__(self):
        """sqlalchemy result proxies for sql expressions give dict like objects
        that also are iterable like lists... Unfortunately openpyxl needs
        instances of list or tuple... let's make it happy
        """
        transformer = self.transformer
        for row in self.iterator:
            yield [
                transformer.apply(item, index=i) for i, item in enumerate(row)
            ]


class List2Dict(object):
    """a stream adapter the takes an iterable containing lists (or list like
     iterables) and returns another iterable containing dictionaries.
    This works by using indexes to map to certain attributes

    the mapping should be a simple dict giving the target attr name as a value
    stored under the index it can be found in the original list:

    imagin a list l and a mapping:
    >>> l = [
    ...    [u'Florent', u'3 rue des petits chats', u'Paris', u'florent@here'],
    ... ]
    >>> mapping = {0: 'name', 1: 'street', 3: 'email'}
    >>> adapted = List2Dict(l, mapping)
    >>> for item in adapted:
    ...     assert item['name'] == u'Florent'
    ...     assert item['street'] == u'3 rue des petits chats'
    ...     assert item.get('email', None) == u'florent@here'
    """

    def __init__(self, iterator, attrsmapping):
        self.iterator = iterator
        self.attrsmapping = attrsmapping

    def __iter__(self):
        mapping = self.attrsmapping
        for row in self.iterator:
            yield {
                attrname: row[index] for (index, attrname) in mapping.items()
            }


class Obj2List(BaseAdapter):
    """an adapter that takes an iterator and a list of attributes.
    The given iterator should yield objects that contain the attributes
    referenced in your given attribute list.

    It then gives you a new iterator that yields lists of items, according
    to the list of attributes you gave to the constructor.

    it accepts an instance of transformer as an optional parameter.

    Transformers are available in any2.transformers
    """

    def __init__(self, iterator, attrs, transformer=None):
        """Constructor for an objetc to list adapter

        :param iterator: the iterator to adapt
        :param attrs: a list of attributes present on the objects yielded by
        the provided iterator
        :param transformer: an optional any2.transformers.BaseTransformer
        instance
        :return: an adapted iterator that yields lists. Each yielded list
        contains as many items as the attrs list given to the constructor.
        """
        self.attrs = attrs
        super(Obj2List, self).__init__(iterator, transformer=transformer)

    def __iter__(self):
        transformer = self.transformer
        attrs = self.attrs
        for row in self.iterator:
            yield [
                transformer.apply(item, index=i)
                for i, item in enumerate(
                    [recursive_getattr(row, name) for name in attrs]
                )
            ]


class DictAdapter(object):
    """An adapter that will make sure the provided object exposes
    attributes and methods that are useable by a csv.DictWriter instance,
    basically adapting any python object to give it a dictionary signature.
    """

    def __init__(self, obj, column_mappings):
        """Initialize a CSVAddon
        @param obj: The object to be adapted.
        @type obj: any python object instance

        @param column_mappings:
        @type column_mappings: list of dictionary
        """
        self.obj = obj
        self.column_mappings = column_mappings

        self.__col_maps = dict()
        self.__init_column_maps()

    def __init_column_maps(self):
        for colmap in self.column_mappings:
            self.__col_maps[colmap['colname']] = colmap

    def __iter__(self):
        """Dictionary method needed by the DictWriter
        """
        for k in self.__col_maps.keys():
            yield k

    def keys(self):
        """Dictionary method needed by the DictWriter
        """
        return self.__col_maps.keys()

    def items(self):
        """dictionary method need by Any2CSV
        """
        for k in self.__col_maps.keys():
            yield (k, self.get(k, u''))

    def get(self, column_name, default_value):
        """Dictionary method needed by the DictWriter
        """
        column_mapping = self.__col_maps[column_name]
        attr = column_mapping.get('attr', None)
        renderer = column_mapping.get('renderer', None)

        if attr is not None:
            value = recursive_getattr(self.obj, attr, default_value)

        else:
            value = None

        if renderer is not None:
            if callable(renderer):
                # those imports are here because the renderer can be a
                # one liner # function defined by someone who
                # cannot import those. don't remove the unused imports
                import decimal
                import datetime
                try:
                    value = renderer(value=value)
                except Exception as e:
                    msg = 'Error during rendering %s with value %s : %s' % (
                        column_name, value, e
                    )
                    log.exception(msg)

            elif (
                    isinstance(renderer, six.string_types)
            ):
                # case when the caller has defined a renderer as a static
                # string effectively ignoring the real value
                value = renderer
            else:
                msg = 'Renderer should be callable or string, not %s' % type(
                    renderer)
                raise ColumnMappingError(msg)

        if value is None:
            # TODO: should we REALLY return an empty string here?
            value = u''

        return value
