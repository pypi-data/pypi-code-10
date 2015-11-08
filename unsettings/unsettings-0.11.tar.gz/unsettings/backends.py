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

from gi.repository import Gio, GLib, GConf as gconf

import re, itertools, logging, subprocess, os, os.path

import settings, zgutils


class NoDefaultValueException(Exception):
    pass

class Backend(object):

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def set_default(self):
        raise NotImplementedError

    def get_default(self):
        raise NotImplementedError

    def values(self):
        return [self[x] for x in self.keys()]
    
    def items(self):
        return [(x, self[x]) for x in self.keys()]

    def __getitem__(self, key):
        """
        x.__getitem__(y) <==> x[y]
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """
        x.__setitem__(i, y) <==> x[i]=y
        """
        self.set(key, value)    
        
    def __len__(self):
       """
       x.__len__() <==> len(x)
       """
       return len(self.keys())
        

class CombinedDict(Backend):
    def __init__(self):
        self.backends = {}

    def create_backend_for_scheme(self, scheme):
        if scheme == 'gsettings':
            return GSettingsDict()
        elif scheme == 'gconf':
            return GConfDict()
        elif scheme == 'env':
            return EnvFileDict()
        elif scheme == 'zeitgeist':
            return ZeitgeistDict()
        elif scheme == 'xkbopt':
            return XKBOptsDict()
        elif scheme == 'userdir':
            return UserDirsDict()
        else:
            print('Scheme %s not supported'%scheme)
            
    def parse_key(self, key):
        (scheme, name) = key.split(':', 1)
        if name.startswith('//'):
            name = name[1:]
        return scheme, name

    def get(self, key):
        #print 'CD.get:', key
        scheme, name = self.parse_key(key)
        #print 'CD.get s,n:', scheme, name
        if not scheme in self.backends:
            self.backends[scheme] = self.create_backend_for_scheme(scheme)
        #print 'CD.get end', self.backends[scheme].get(name)  
        return self.backends[scheme].get(name)        
        
    def set(self, key, value):
        scheme, name = self.parse_key(key)
        if not scheme in self.backends:
            self.backends[scheme] = self.create_backend_for_scheme(scheme)
        self.backends[scheme].set(name, value)
        
    def set_default(self, key):
        scheme, name = self.parse_key(key)
        if not scheme in self.backends:
            self.backends[scheme] = self.create_backend_for_scheme(scheme)
        self.backends[scheme].set_default(name)

    def get_default(self, key):
        scheme, name = self.parse_key(key)
        if not scheme in self.backends:
            self.backends[scheme] = self.create_backend_for_scheme(scheme)
        return self.backends[scheme].get_default(name)

class GSettingsDict(Backend):
    def __init__(self, autosync = True):
        self.gsettings = {}
        self.autosync = autosync
     
    def parse_key(self, key):
        if key.startswith('/'):
            key = key[1:]        
        base, name = key.split(' ', 1)
        try:
            scheme, path = base.split(':', 1)
        except ValueError:
            scheme = base
            path = ''
        gid = base
        #print 'PK:', '|'.join([key, base, gid, scheme, path, name])
        return gid, scheme, path, name

    def get_gsettings(self, key):
        gid, scheme, path, name = self.parse_key(key)
        try:
            return self.gsettings[gid]
        except KeyError:
            if ((path != '' and 
                scheme in Gio.Settings.list_relocatable_schemas()) or 
               (scheme in Gio.Settings.list_schemas())):
                if path:
                   self.gsettings[gid] = Gio.Settings.new_with_path(scheme, 
                                                                    path) 
                else:
                    self.gsettings[gid] = Gio.Settings.new(scheme)
                return self.gsettings[gid]
            else:
               print 'ERROR: no schema', scheme

    def get(self, key):
        gid, scheme, path, name = self.parse_key(key)
        settings = self.get_gsettings(key)
        if settings is not None and name in settings.list_keys():
            value = settings.get_value(name).unpack()
        else:
            print 'ERROR: no key', scheme, path, key
            value = None
        return  value

    def set(self, key, value):
        gid, scheme, path, name = self.parse_key(key)
        settings = self.get_gsettings(key)
        if settings is not None:
            type_string = settings.get_value(name).get_type_string() 
            try:
                settings.set_value(name, GLib.Variant(type_string, value))
                self.sync(key)
            except Exception as e:
                  logging.error('Error setting "%s" to "%s": %s' % (
                      key, value, e))
            

    def set_default(self, key):
        gid, scheme, path, name = self.parse_key(key)
        settings = self.get_gsettings(key)
        if settings is not None:
            settings.reset(name)
            self.sync(key)

    def get_default(self, key):
        # old = self.get(key)
        gid, scheme, path, name = self.parse_key(key)
        settings = self.get_gsettings(key)
        if settings is not None and name in settings.list_keys():
            try:
                value = settings.get_default_value(name).unpack()
            except AttributeError:  # old Gio.Settings
                logging.debug('GET DEFAULT %s: old way' % key)
                old = self.get(key)
                settings.reset(name)
                value = self.get(key)
                self.set(key, old)
        else:
            print 'ERROR: no key', scheme, path, key
            value = None
        return  value


    def add_listener(self, key, func):
        self.get_gsettings(key).connect('changed::%s' % key, func, self)

    def remove_listener(self, key, func):
        self.get_gsettings(key).unconnect('changed::%s' % key, func)

    def sync(self, key):
        self.get_gsettings(key).sync()

    def keys(self):
        keys = []
        for (base, gsettings) in  self.gsettings:
            keys.extend(["%s/%s" % (base, x) for x in  gsettings.list_keys()])
        return keys
        
      
class GConfDict(Backend):
    def __init__(self, dir=None):
        if dir is None:
            dir = ''
        
        self.dir = dir.rstrip('/')
        self.gclient = gconf.Client.get_default()
        if self.dir != '':
            self.gclient.add_dir(self.dir.rstrip('/'), 
                                 gconf.ClientPreloadType.PRELOAD_NONE)
            

    def normalize_key(self, key):
        """
        Expands relativ keys if needed
        """
        if len(key) > 0 and key[0] != '/':
            key='%s/%s'%(self.dir, key)
        return key
    
    def normalize_dir(self, dir):
        """
        Expands relativ dirs if needed
        """
        if dir == '':
            return '/'
        else:
            return dir.rstrip('/')
        
    def get(self, key):
        """
        Returns the value for `key`
        """
        return self.to_python(self.gclient.get(self.normalize_key(key)))

    def set(self, key, value):
        """
        Set value for `key` to `value`
        """
        self.gclient.set(self.normalize_key(key), self.from_python(value))
        self.sync()
            
    def set_default(self, key):
        """
        Set value for `key` to default value
        """
        key = self.normalize_key(key)
        value = self.gclient.get_default_from_schema(key)
        if value is not None:
            self.gclient.set(key, value)
        self.sync()
            
    def get_default(self, key):
        """
        Set value for `key` to default value
        """
        key = self.normalize_key(key)
        gvalue = self.gclient.get_default_from_schema(key)
        if gvalue is None:
            raise NoDefaultValueException
        return self.to_python(gvalue)

    def unset(self, key):
        """
        Unset `key`
        """
        key = self.normalize_key(key)
        self.gclient.unset(key)

    def sync(self):
        """
        Suggests to gconfd that you've just finished a block of
        changes, and it would be an optimal time to sync to permanent
        storage. This is only a suggestion; and gconfd will eventually
        sync even if you don't call sync(). This
        function is just a "hint" provided to gconfd to maximize
        efficiency and minimize data loss.
        """
        self.gclient.suggest_sync()
        self.gclient.clear_cache()
            
    def add_listener(self, key, func, *args):
        """
        Request notification of changes to key

        - `func`: function to call when changes occur.
                  It's called as func(key, value, gconfdict, id, args)
        - `args`: user data to pass to func

        The function returns a connection ID you can use to call
        remove_listener()
        """
        key = self.normalize_key(key)

        def foo(client, id, entry, *args):
            func(entry.key, self.to_python(entry.value), self, id, *args)

        return self.gclient.notify_add(key, foo, args)

    def remove_listener(self, id):
        """
        Remove a notification using the ID returned from add_listener()
        
        - `id`: connection ID returned from add_listener()
        """
        self.gclient.notify_remove(id)

    def has_key(self, key):
        """
        True if `key` is defined and not a dir
        """
        return self.normalize_key(key) in self.keys()
    
    def to_python(self, gcvalue):
        """
        Convert a gconf value to a python value
        Arguments:
        - `gcvalue`: a gconf value
        """
        if gcvalue is None:
            return None
        else:
            _type=gcvalue.type
            if _type is gconf.ValueType.LIST:
                return tuple(self.to_python(v) for v in gcvalue.get_list())
            elif _type is gconf.ValueType.PAIR:
                return self.to_python(gcvalue.get_car()), self.to_python(gcvalue.get_cdr())
            else:
                return getattr(gcvalue, 'get_%s'%_type.value_nick)()

    def from_python(self, value):
        """
        Convert a Python value to a gconf value
        """
        if isinstance(value, basestring):
            val=gconf.Value.new(gconf.ValueType.STRING)
            val.set_string(value)
        elif isinstance(value, bool):
            val=gconf.Value.new(gconf.ValueType.BOOL)
            val.set_bool(value)
        elif isinstance(value, int) or  isinstance(value, long):
            val=gconf.Value.new(gconf.ValueType.INT)
            val.set_int(value)
        elif isinstance(value, float):
            val=gconf.Value.new(gconf.ValueType.FLOAT)
            val.set_float(value)       
        elif isinstance(value, tuple) and len(value)==2:
            val=gconf.Value.new(gconf.ValueType.PAIR)
            val.set_car(self.from_python(value[0]))
            val.set_cdr(self.from_python(value[1]))
        elif isinstance(value, list) or  isinstance(value, tuple):
            val=gconf.Value.new(gconf.ValueType.LIST)
            l=[self.from_python(v) for v in value]
            if len(l) > 0:
                val.set_list_type(l[0].type)
            val.set_list(l)
        else: raise ValueError()
        return val

    def iterkeys(self):
        """
        return an iterator over the keys
        """
        for v in self.gclient.all_entries(self.normalize_dir(self.dir)):
            yield v.key

    def keys(self):
        """
        return a list of all keys
        """
        return tuple(self.iterkeys())


    def itervalues(self):
        """
        return an iterator over the values
        """
        for v in self.gclient.all_entries(self.dir):
            yield self.to_python(v.value())

    def values(self):
        """
        return a list of all values
        """
        return tuple(self.itervalues())

    def iteritems(self):
        """
        return an iterator over (key, value) pairs
        """
        for v in self.gclient.all_entries(self.dir):
            yield v.key, self.to_python(v.value)

             
    def iterdirs(self):
        """
        return an iterator over the subdirs
        """
        for d in self.gclient.all_dirs(self.dir):
            yield d

    def dirs(self):
        """
        return a list of all subdirs
        """  
        return tuple(self.iterdirs())
    
        
    def children(self):
        """
        return a list of all sudbirs and keys
        """
        return self.dirs()+self.keys()

    
    def __getitem__(self, key):
        """
        x.__getitem__(y) <==> x[y]
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """
        x.__setitem__(i, y) <==> x[i]=y
        """
        self.set(key, value)

    def  __iter__(self):
        """
        x.__iter__() <==> iter(x)
        """
        return self.iterkeys()

    def __delitem__(self, key):
        """
        x.__delitem__(y) <==> del x[y]
        """
        self.delete(key)

    def __len__(self):
        """
        x.__len__() <==> len(x)
        """
        return len(self.keys())    

    def __contains__(self, item):
        """self.data_key
        x.__contains__(y) <==> y in x
        """
        return self.has_key(item)



class EnvFileDict(Backend):
    def __init__(self):
        self.path = settings.X_ENV_FILE
        self.data = dict()
        self.regex = re.compile("export (?P<key>\w+)='(?P<value>\S*)'")

    def _read(self, key):
        if key in self.data:
            return
        d = dict()
        try:
            with open(self.path, 'r') as f:
                for line in f:
                    match = self.regex.match(line)
                    if match:
                        _key, value = match.group('key', 'value')
                        if key == _key:
                            d[_key] = value
        except IOError:
            pass
        self.data = d


    def _write(self):
        with open(self.path, 'w') as f:
            f.write("## created by %s v%s\n"%(settings.APP_NAME, 
                                            settings.APP_VERSION))
            f.write("## *** DO NOT MODIFY ***\n")
            for key, value in self.data.iteritems():
                f.write("export %s='%s'\n"%(key, value))
    
    def parse_key(self, key):
        if key.startswith('/'):
            key = key[1:]
        return key

    def get(self, key):
        key = self.parse_key(key)
        self._read(key)
        return self.data.get(key, None)

    def set(self, key, value):
        key = self.parse_key(key)
        if value is None:
            if key in self.data:
                del self.data[key]
        else:
            self.data[key] = value
        self._write()

    def set_default(self, key):
        key = self.parse_key(key)
        if key in self.data:
            del self.data[key]
        self._write()

    def get_default(self, key):
        return None
                 
        

class ZeitgeistDict(Backend):

        
    def get(self, key):
        if key == '/enabled':
            return zgutils.zeitgeist_is_enabled()
     

    def set(self, key, value):
        if key == '/enabled':
            if value:
                zgutils.zeitgeist_enable()
            else:
                zgutils.zeitgeist_disable()

    def set_default(self, key):
        if key == '/enabled':
            self.set(key, True)

    def get_default(self, key):
      if key == '/enabled':
          return True

    def keys(self):
        return ['/enabled']


class XKBOptsDict(Backend):

    def __init__(self):
        scheme = 'org.gnome.desktop.input-sources'
        self.key = 'xkb-options'
        self.gsettings = Gio.Settings.new(scheme)


    def _get_options(self):
        value = self.gsettings.get_value(self.key).unpack()
        return value

    def _set_options(self, options):
        type_string = self.gsettings.get_value(self.key).get_type_string()
        #print('XKB:', options)
        self.gsettings.set_value(self.key, GLib.Variant(type_string, options))
        self.gsettings.sync()

    def get(self, key):
        key = '%s:' % key.lstrip('/')
        options = self._get_options()
        try:
            result = filter(lambda i: i.startswith(key), options)[0]
            result = result.split(':')[1]
        except IndexError:
            result = '---'
        #print('GET:', key, result)
        return result
        
    def set(self, key, value):
        options = self._get_options()
        key = '%s:' % key.lstrip('/')
        newopts = filter(lambda i: not i.startswith(key), options)
        if value != '---':
            newopts.append('%s%s' % (key, value))
        self._set_options(newopts)


    def set_default(self, key):
        self.set(key, '---')

    def get_default(self, key):
        return '---'

    def keys(self):
        return self._get_options()

    
class UserDirsDict(Backend):

    def __init__(self):
        self.homedir = os.path.expanduser('~/')
    
    def get(self, key):
        key = key.lstrip('/')
        try:
            dir = subprocess.check_output(['/usr/bin/xdg-user-dir', key])
        except EnvironmentError as e:
            logging.warn('UserDir get %s:  %s' %( key, e))
            return None
        return dir.rstrip('\n')

    def set(self, key, value):
        key = key.lstrip('/')
        if not value.startswith('/'):
            value = os.path.join(self.homedir, value)
        try:
            subprocess.check_output(['xdg-user-dirs-update', '--set', key, value])
            os.makedirs(value)
        except OSError as e:
            if  e.errno not in (17,): # already exists
                logging.warn('UserDir get %s=%s:  %s' %(key, value, e))
        except EnvironmentError as e:
            logging.warn('UserDir get %s=%s:  %s' %(key, value, e))

    def set_default(self, key):
        key = key.lstrip('/')
        print('userdir set_default')
        return

    def get_default(self, key):
        key = key.lstrip('/')
        print('userdir get_default')
        return self.homedir

            
if __name__ == '__main__':
    ud = UserDirsDict()
    for i in ('DESKTOP', 'PICTURES', 'FOOBAR'):
        print(i, ':', ud.get(i))
        
    for i in ('DESKTOP', 'PICTURES', 'FOOBAR'):
        print('set:', i)
        print(ud.set(i, i))
        print(ud.get(i))
