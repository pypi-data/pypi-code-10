"""
Module contains helper functions for name operations.
"""

import inspect
import sys
import os


def mangle_name(owning_class, attr: str) -> str:
    """
    Mimic Python's name mangling for attributes that name starts with double underscore.
    """

    return '_{}__{}'.format(
        owning_class if type(owning_class) is str else owning_class.__name__,
        attr
    )


def unmangle_name(name: str) -> str:
    """
    Return unmangled name
    """

    try:
        return name.split('__')[1]
    except IndexError:
        return name


def get_object(location: str) -> object:
    """
    Return object by its location within current module.
    Useful to access objects that haven't bind to local or global namespace yet.

    :param location: dotted name, eg. Foo or Foo.Bar
    :return: object within current module
    """

    stack = inspect.stack()[1:]

    def _get_from_scope():
        path, _, symbol_name = location.rpartition('.')

        for stack_item in stack:
            f_locals = stack_item[0].f_locals
            qualname = f_locals.get('__qualname__')

            if qualname is None:
                continue

            if not qualname.startswith(path):
                break

            if qualname == path:
                return f_locals.get(symbol_name)

    def _get_module_from_stack(stack):
        module_path = stack[0][1]
        matches = [module_path[len(path)+1:] for path in sys.path if module_path.startswith(path)]
        matches.sort(reverse=True)
        module = None

        for match in matches:
            try:
                match_without_ext = "".join(match.split('.')[:-1])
                module_name = ".".join(match_without_ext.split(os.sep))
                module = sys.modules[module_name]
            except KeyError:
                pass

        return module

    def _get_from_globals():
        calling_module = _get_module_from_stack(stack) # inspect.getmodulename fails in some cases

        try:
            cls = calling_module

            for part in location.split('.'):
                cls = getattr(cls, part)

            return cls
        except AttributeError:
            return None

    cls = _get_from_scope() or _get_from_globals()

    if cls is not None:
        return cls
    else:
        raise NameError("'{}' is invalid reference".format(location))
