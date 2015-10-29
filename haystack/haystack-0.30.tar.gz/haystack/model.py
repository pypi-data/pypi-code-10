# -*- coding: utf-8 -*-
#
# Copyright (C) 2011,2012,2013 Loic Jaquemet loic.jaquemet+python@gmail.com
#

"""
Defines
        CTypesRecordConstraintValidator
        LoadableMembersStructure
        LoadableMembersUnion
        CString.

        helpers function to import allocators or to create duplicate
Plain Old Python Objects from ctypes allocators modules.

    NotValid(Exception)
    LoadException(Exception)
"""

__author__ = "Loic Jaquemet"
__copyright__ = "Copyright (C) 2013 Loic Jaquemet"
__email__ = "loic.jaquemet+python@gmail.com"
__license__ = "GPL"
__maintainer__ = "Loic Jaquemet"
__status__ = "Production"

import ctypes
import inspect
import sys
import logging
import importlib

from haystack import target

log = logging.getLogger('model')


class NotValid(Exception):
    pass


class LoadException(Exception):
    pass


class Model(object):

    def __init__(self, memory_handler):
        self._memory_handler = memory_handler
        self.__book = dict()
        self.__modules = dict()

    def reset(self):
        """Clean the book"""
        log.info('RESET MODEL')
        self.__book = dict()
        # FIXME: that is probably useless now.
        for mod in sys.modules.keys():
            if 'haystack.reverse' in mod:
                del sys.modules[mod]
                log.debug('de-imported %s',mod)

    def __create_POPO_classes(self, targetmodule):
        """ Load all model classes and create a similar non-ctypes Python class
            thoses will be used to translate non pickable ctypes into POPOs.

            Mandatory.
        """
        _ctypes = self._memory_handler.get_target_platform().get_target_ctypes()
        _created = 0
        for name, klass in inspect.getmembers(targetmodule, inspect.isclass):
            # we only need to create python classes for records
            if issubclass(klass, _ctypes.Structure) or issubclass(klass, _ctypes.Union):
                from haystack.outputters import python
                # we have to keep a local (model) ref because the class is being created here.
                # and we have a targetmodule ref. because it's asked.
                # and another ref on the real module for the basic type, because,
                # that is probably were it's gonna be used.
                ## full namespace
                if True:
                    # that creates a haystack.model.x.x.x.classname_py
                    kpy = type('%s.%s_py' % (targetmodule.__name__, name), (python.pyObj,), {})
                    setattr(sys.modules[__name__], '%s.%s_py' % (targetmodule.__name__, name), kpy)
                    # because we use it from the target module in our code
                    setattr(targetmodule, '%s_py' % name, kpy)
                ## partial namespace
                else:
                    kpy = type('%s_py' % name, (python.pyObj,), {})
                    setattr(sys.modules[__name__], '%s_py'% name, kpy )
                    setattr(targetmodule, '%s_py' % name, kpy)

                # add the structure size to the class
                setattr(kpy, '_len_', _ctypes.sizeof(klass))
                _created += 1
        log.debug(
            'created %d POPO types in %s' %
            (_created, targetmodule.__name__))
        return _created

    def build_python_class_clones(self, targetmodule):
        """Registers a module that contains ctypes records.

        Mandatory call that will be done by haystack scripts.

        Ctypes modules are not required to register themselves, as long as haystack
        framework does it.

        The only real action is to :
        - Creates Plain old python object for each ctypes record to be able to
        pickle/unpickle them later.
        """
        log.debug('registering module %s', targetmodule)
        if targetmodule in self.get_pythoned_modules().values():
            log.warning('Module %s already registered. Skipping.', targetmodule)
            return
        module_name = targetmodule.__name__
        if module_name in self.get_pythoned_modules().keys():
            log.warning('Module %s already registered. Skipping.', module_name)
            return
        _registered = self.__create_POPO_classes(targetmodule)
        if _registered == 0:
            log.warning(
                'No class found. Maybe you need to model.copy_generated_classes ?')
        # register once per session.
        self.__book[module_name] = targetmodule
        log.debug('registered %d modules total', len(self.__book.keys()))
        return

    def get_pythoned_modules(self):
        return self.__book

    def get_pythoned_module(self, name):
        return self.__book[name]

    def import_module(self, module_name):
        """
        Import the python ctypes module with this target ctypes platform.

        :param module_name:
        :return:
        """
        _ctypes = self._memory_handler.get_target_platform().get_target_ctypes()
        mod = import_module_for_target_ctypes(module_name, _ctypes)
        self.__modules[module_name] = mod
        return mod

    def get_imported_modules(self):
        """
        :return: the module that have been imported
        """
        return self.__modules

    def get_imported_module(self, name):
        """
        :return: the module that have been imported
        """
        return self.__modules[name]


def copy_generated_classes(src_module, dst_module):
    """Copies the ctypes Records of a module into another module.
    Is equivalent to "from src import *" but with less clutter.
    E.g.: Enum, variable and functions will not be imported.

    Calling this method is facultative.

    :param src_module : src module, generated
    :param dst_module : dst module
    """
    log.debug('copy classes %s -> %s' % (src_module.__name__, dst_module.__name__))
    copied = 0
    for (name, klass) in inspect.getmembers(src_module, inspect.isclass):
        if issubclass(klass, ctypes.Structure) or issubclass(klass, ctypes.Union):
            log.debug("setattr(%s,%s,%s)" % (dst_module.__name__, name, klass))
            setattr(dst_module, name, klass)
            copied += 1
        else:
            log.debug("drop %s - %s" % (name, klass))
            pass
    log.debug('Loaded %d C structs from src %s' % (copied, src_module.__name__))
    log.debug(
        'There is %d members in src %s' %
        (len(
            src_module.__dict__),
            src_module.__name__))
    return


def import_module_for_target_ctypes(module_name, target_ctypes):
    """
    Import the python ctypes module for a specific ctypes platform.

    :param module_name: module
    :param _target: ICTypesProxy
    :return:
    """
    # save ctypes
    real_ctypes = sys.modules['ctypes']
    sys.modules['ctypes'] = target_ctypes
    if module_name in sys.modules:
        del sys.modules[module_name]
    my_module = None
    try:
        # try to load that module with our ctypes proxy
        my_module = importlib.import_module(module_name)
        # FIXME debug and TU this to be sure it is removed from modules
        #if module_name in sys.modules:
        #    del sys.modules[module_name]
    finally:
        # always clean up
        sys.modules['ctypes'] = real_ctypes
    return my_module
