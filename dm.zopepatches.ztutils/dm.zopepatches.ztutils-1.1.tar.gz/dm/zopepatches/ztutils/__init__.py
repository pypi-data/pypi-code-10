"""ZTUtils improvements."""
from json import loads, dumps
from types import NoneType

from DateTime.DateTime import DateTime
from ZPublisher.Converters import type_converters
from ZPublisher.HTTPRequest import record

from logging import getLogger
logger = getLogger('dm.zopepatches.ztutils')

_extensions = []

# handle tuple and unicode
def complex_marshal(pairs):
    '''Add request marshalling information to a list of name-value pairs.

    Names must be strings.  Values may be strings, unicode,
    booleans, integers, floats, or DateTimes, and they may also be tuples, lists or
    namespaces containing these types.
    You can register extensions to support more elementary types
    of more deeply nested structures.

    The list is edited in place so that each (name, value) pair
    becomes a (name, marshal, value) triple.  The middle value is the
    request marshalling string.  Integer, float, and DateTime values
    will have ":int", ":float", or ":date" as their marshal string.
    Lists will be flattened, and the elements given ":list" in
    addition to their simple marshal string.  Dictionaries will be
    flattened and marshalled using ":record".
    '''
    def simple_marshal(v):
        """pair specifying the request marshal string and the transformed value."""
        if isinstance(v, str):
            return '', v
        if isinstance(v, unicode):
            return ':utf8:ustring', v.encode('utf-8')
        if isinstance(v, bool):
            return ':boolean', v
        if isinstance(v, int):
            return ':int', v
        if isinstance(v, float):
            return ':float', v
        if isinstance(v, DateTime):
            return ':date', v
        for e in _extensions:
            ec = e.check
            if ec is None or ec(v):
                return e.type_tag, e.marshal(v)
        # maybe, we should raise an exception here -- as it is likely,
        #   that we do something wrong
        return '', v

    def process_sequence(s, name, suffix=''):
        """a sublist describing marshalling for sequence (list or tuple) *s*."""
        # note: we marshal tuples as "list".
        tag = ':list'
        if not s: return [(name, ':tokens' + suffix, '')] # empty sequence marshalled as tokens
        return [(name, mt + tag + suffix, v)
                for mt, v in map(simple_marshal, s)
                ]
      
    i = len(pairs)
    while i > 0:
        i = i - 1
        k, v = pairs[i]
        m = ''
        sublist = None
        if isinstance(v, str):
            pass
        elif hasattr(v, 'items'):
            sublist = []
            for sk, sv in v.items():
                name = '%s.%s' % (k, sk)
                if isinstance(sv, (list, tuple)):
                    sublist.extend(process_sequence(sv, name, ':record'))
                else:
                    sm, sv = simple_marshal(sv)
                    sublist.append((name, '%s:record' % sm,  sv))
        elif isinstance(v, (list, tuple)):
            sublist = process_sequence(v, k)
        else:
            m, v = simple_marshal(v)
        if sublist is None:
            pairs[i] = (k, m, v)
        else:
            pairs[i:i + 1] = sublist
    return pairs




def register_extension(extension, before=None):
    """register *extension* before the extension with tag *before*.

    If *before* is `None` (or any not yet registered tag),
    the extension is inserted after,
    if it is `'*'` before all already registered extensions.
    """
    i = 0
    if before != '*':
        for i in range(0, len(_extensions)):
            if _extensions[i].tag == before: break
        else: i = len(_extensions)
    _extensions.insert(i, extension)
    extension.register()


def unregister_extension(tag):
    """unregister all extensions with *tag*."""
    _extensions[:] = [e for e in _extensions if not e.tag == tag]


class Extension(object):
    """A marshaling/demarshaling extension.

    Extensions are maintained as a sequence of extensions.
    The first matching extension wins. Therefore, order is important.

    To control the order, extensions have a tag used to identify the extension.
    You can use the tag in `register_extension` (in the `before` parameter)
    and `unregister_extension`.

    An extension has a check, a marshalling and optionally a
    demarshalling function. In addition, it has a `type_tag` used
    as type tags in names providing a communication with the
    `ZPublisher`'s converter facility.

    `check` is applied to the value and returns true when the extension
    applies. In this case, its `marshal` function is applied to the
    value and must return a string representation for the value.
    This string together with `type_tag` is used to represent
    the value in the query string or form.

    If the extension has a demarshalling function, it is registered
    under `type_tag` as a `ZPublisher` converter. Usually, the
    demarshalling approximately reverses the effect of the marshalling.
    """

    def __init__(self, tag, check, marshal, demarshal=None, type_tag=None):
        """see class doc for the parameter semantics.

        *type_tag* defaults to *tag*.
        """
        self.tag, self.check, self.marshal, self.demarshal = \
                  tag, check, marshal, demarshal
        if type_tag is None: type_tag = tag
        self.converter_tag = type_tag
        if type_tag: type_tag = ":" + type_tag
        self.type_tag = type_tag

    def register(self):
        if self.demarshal:
            def conv(v, demarshal=self.demarshal):
                if hasattr(v, "read"): v = v.read()
                return demarshal(v)
            type_converters[self.converter_tag] = conv

# JSON based marshalling/demarshalling
def support_record_json_marshalling(o):
    if isinstance(o, record): return dict(o)
    raise TypeError("cannot (json) marshal %s" % repr(o))

def register_json_extension(before=None):
    register_extension(
        Extension("json",
                  lambda v: isinstance(
                      v,
                      (basestring, bool, int, long, float, list, tuple, dict,
                       record,
                       )
                      ),
                  lambda v: dumps(v, default=support_record_json_marshalling),
                  loads
                  ),
        before
        )

# `None` support
def register_none_extension(before='*'):
    register_extension(
        Extension("none",
                  lambda v: v is None,
                  lambda v: '',
                  lambda v: None,
                  ),
        before
        )
# by default, register this extension - use `unregister_extension("none")
#  if this change in behavior is unwanted for your application
register_none_extension()


logger.info('ZTUtils.Zope.complex_marshal patch: now handles tuples and unicode and supports extensions.')

from ZTUtils import Zope
Zope.complex_marshal = complex_marshal
    
