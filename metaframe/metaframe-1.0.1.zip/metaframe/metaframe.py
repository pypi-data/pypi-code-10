#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class MetaFrame(type):
    '''This Metaclass intercepts instance creation/initialization enabling use
    cases like modification of args, kwargs and/or scanning of the object post
    init
    '''

    def _new_pre(cls, *args, **kwargs):
        '''Called before the object is created.

        Args:
          cls (automatic): The class which is going to be instantiated
          args: To be passed to ``__new__`` for class instantiation
          kwargs: To be passed to ``__new__`` for class instantiation

        Returns:
          cls, args, kwargs as a tuple

        The return values need not be the same that were passed
        '''
        return cls, args, kwargs

    def _new_do(cls, *args, **kwargs):
        '''Called for object creation

        Args:
          cls (automatic): The class which is going to be instantiated
          args: To be passed to ``__new__`` for class instantiation
          kwargs: To be passed to ``__new__`` for class instantiation

        Returns:
          obj, args, kwargs as a tuple

        Note that in this method the 1st return value is no the 1st
        passed argument (unlike in the rest of methods) It is the created
        instance and not the passed class

        The return values need not be the same that were passed
        '''
        obj = cls.__new__(cls, *args, **kwargs)
        return obj, args, kwargs

    def _init_pre(cls, obj, *args, **kwargs):
        '''Called after object creation and before the object is init'ed

        Args:
          - cls (automatic): The class which has been instantiated
          - obj: The class instance which has been created
          - args: To be passed to ``__init__`` for object initialization
          - kwargs: To be passed to ``__init__`` for object initialization

        Returns:
          obj, args, kwargs as a tuple

        The return values need not be the same that were passed
        '''
        return obj, args, kwargs

    def _init_do(cls, obj, *args, **kwargs):
        '''Called for object initialization

        Args:
          - cls (automatic): The class which has been instantiated
          - obj: The class instance which has been created
          - args: To be passed to ``__init__`` for object initialization
          - kwargs: To be passed to ``__init__`` for object initialization

        Returns:
          obj, args, kwargs as a tuple

        The return values need not be the same that were passed
        '''
        obj.__init__(*args, **kwargs)
        return obj, args, kwargs

    def _init_post(cls, obj, *args, **kwargs):
        '''Called after object initialization

        Args:
          - cls (automatic): The class which has been instantiated
          - obj: The class instance which has been created
          - args: Which were passed to ``__init__`` for object initialization
          - kwargs: Which were passed to ``__init__`` for object initialization

        Returns:
          obj, args, kwargs as a tuple

        The return values need not be the same that were passed. But modifying
        ``args`` and/or ``kwargs`` no longer plays a role because the object
        has already been created and initialized
        '''
        return obj, args, kwargs

    def __call__(cls, *args, **kwargs):
        '''Creates an initializes an instance of cls calling the pre-new,
        pre-init/post-init hooks with the passed/returned ``args`` / ``kwargs``
        '''
        # Before __new__ (object not yet created)
        cls, args, kwargs = cls._new_pre(*args, **kwargs)

        # Create the object
        obj, args, kwargs = cls._new_do(*args, **kwargs)

        # Before __init__
        obj, args, kwargs = cls._init_pre(obj, *args, **kwargs)

        # Init the object
        obj, args, kwargs = cls._init_do(obj, *args, **kwargs)

        # After __init__
        obj, args, kwargs = cls._init_post(obj, *args, **kwargs)

        # Return the created & init'ed object
        return obj

    @classmethod
    def as_metaclass(meta, *bases):
        '''Create a base class with "this metaclass" as metaclass

        Meant to be used in the definition of classes for Py2/3 syntax equality

        Args:
          bases: a list of base classes to apply (object if none given)
        '''
        class metaclass(meta):

            def __new__(cls, name, this_bases, d):
                # subclass to ensure super works with our methods
                # mt = type(str('xxxxx'), (meta,), {})
                return meta(name, bases, d)
        return type.__new__(metaclass, str('tmpcls'), (), {})

    # This is from Armin Ronacher from Flask simplified later by six
    @staticmethod
    def with_metaclass(meta, *bases):
        """Create a base class with a metaclass."""
        # This requires a bit of explanation: the basic idea is to make a dummy
        # metaclass for one level of class instantiation that replaces itself
        # with the actual metaclass.
        class metaclass(meta):

            def __new__(cls, name, this_bases, d):
                return meta(name, bases, d)
        return type.__new__(metaclass, str('tmpcls'), (), {})


class MetaFrameBase(MetaFrame.as_metaclass(object)):
    '''Enables a class to MetaFrame-enabled through inheritance without having
    to specify/declare a metaclass
    '''
    pass
