#-*- coding: utf-8-*-
#
# Unsettings - a configuration frontend for the Unity desktop environment
#
# Copyright (C) 2012 Florian Diesch <devel@florian-diesch.de>
#
# Homepage: http://www.florian-diesch.de/software/unsettings/
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

import widgets, settings, backends
from converter import Converter as DefaultConverter

import logging

BACKEND_DEFAULT=object()

class Connection(object):
    def __init__(self, data_store, data_key, widget, 
                 converter=None, validator=None, default=BACKEND_DEFAULT, 
                 ):
        self.data_store = data_store
        self.data_key = data_key
        self.widget = widget
        if converter is None:
            self.converter = DefaultConverter()
        else:
            self.converter = converter
        self.validator = validator
        self.default = default

        
    def get_widget(self):
        return self.widget

    def get_value(self):
        #print 'GETV:', self.data_store
        try:
            value = self.converter.rev_convert(
                self.data_store[self.data_key])
            #print('GETV:', self.data_key, self.data_store[self.data_key], 
            #      value)
            return value
        except Exception, e:
            print '**get_value: %s (%s)'%(e, self.data_key)

    def get_widget_value(self):
        try:
            return self.converter.convert(self.get_widget().get_data())
        except Exception, e:
            print 'get_widget_value: %s (%s)'%(e, self.data_key)
              
    def set_widget_value(self, value):
        value = self.converter.rev_convert(value)
        try:
            self.get_widget().set_data(value)
        except Exception, e:
            logging.error('Error setting widget "%s" to "%s": %s' % (
                self.data_key, repr(value), e))

    def set_value(self, value):
        #print('SETV:', self.data_key, value)
        try:
            value =  self.converter.convert(value)
            self.data_store[self.data_key] = value
        except Exception as e:
            logging.error('Error setting "%s" to "%s": %s' % (
                self.data_key, repr(value), e))

    def is_dirty(self):        
        try:
            old_value = self.get_value()
            old = self.converter.convert(old_value)
            new = self.get_widget_value()
            logging.debug('IS_DIRTY %s for %s: OLD=%s [%s] NEW=%s' % (
                old != new, self.data_key, old_value, old, new))
            return old != new
        except Exception as e:
            logging.error('IS_DIRTY ERROR "%s" for %s: OLD=%s [%s] NEW=%s' % (
                e, self.data_key, old_value, old, new))
            return None

    def has_key(self, key):
        return self.data_key == key

    def view(self):
        value = self.get_value()
        try:
            self.get_widget().set_data(value)
        except Exception as e:
            logging.error('Error viewing "%s" with "%s": %s' % (
                self.data_key, value, e))

    def store(self):      
        self.set_value(self.get_widget().get_data())

    def set_default(self):
        logging.debug('SET DEFAULT for %s: %s' % 
                      (self.data_key, self.default))
        if self.default is BACKEND_DEFAULT:
            try:
                value = self.data_store.get_default(self.data_key)
            except backends.NoDefaultValueException:
                return
        else:
            value = self.default
        value = self.converter.rev_convert(value)
        logging.debug('SET DEFAULT for %s: value=%s' % 
                      (self.data_key, value))
        self.get_widget().set_data(value)


class ConnectionGroup(object):
    def __init__(self, data_store):
        self.data_store = data_store
        self.connections = []
                    
    def add(self, data_key, widget, converter=None, validator=None, 
            default=BACKEND_DEFAULT):
        conn = Connection(self.data_store, data_key, widget,
                          converter, validator, default)
        self.connections.append(conn)


    def is_dirty(self):
        for conn in self.connections:
            if conn.is_dirty():
                return True
        return False

    def view(self):
        for conn in self.connections:
            conn.view()

    def store(self):
        for conn in self.connections:
            conn.store() 


    def set_defaults(self):
        for conn in self.connections:
            conn.set_default() 
