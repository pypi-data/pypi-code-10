from functools import singledispatch
import types


def define(_doc=None, **funcs):
    '''
    Define protocol.

    :return protocol object with functions defined
    :param _doc: protocol documentation
    :param funcs: map from funtion name to its documentation
    '''
    def fill_class(ns):
        ns['__doc__'] = _doc
        ns['_protocol_functions'] = funcs
        ns.update({
            f_name: staticmethod(_def_disp_function(f_name, f_doc))
            for f_name, f_doc in funcs.items()
        })
        return ns
    return types.new_class('Protocol', exec_body=fill_class)


def register(protocol, type, **funcs):
    '''
    Tie some protocol implementation to given type.

    :param protocol: protocol object
    :param type: dispatch type to register implementation with
    :param funcs: map from funtion name to its implementation.
    '''
    for f_name, f_impl in funcs.items():
        getattr(protocol, f_name).register(type, f_impl)
    assert is_implemented(protocol, type)


def is_implemented(protocol, type):
    '''
    Test if protocol is fully implemented on some type.

    :param protocol: protocol object
    :param type: checked type
    '''
    return all(
        # registered on dispatch function                       ducktype on type
        (type in getattr(protocol, f_name).registry.keys()) or hasattr(type, f_name)
        for f_name in protocol._protocol_functions.keys()
    )


def _def_disp_function(name, doc):
    @singledispatch
    def f(self, *args, **kwargs):
        return getattr(self, name)(*args, **kwargs)
    setattr(f, '__doc__', doc)
    return f
