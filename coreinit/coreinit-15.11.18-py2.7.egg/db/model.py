"""
Copyright (c) 2015 Maciej Nabozny

This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import simplejson
import datetime
import uuid
from coreinit.db import Cache
from coreinit.utils.exceptions import *

class Model(object):
    id = None

    # Key fields, which should be accessible via separate hash maps
    keys = []

    # Serializable fields
    serializable = []

    # The name of cache hash map, which keeps all objects of this type
    container = 'undefined'

    def __init__(self, id=None, data=None):
        if id is not None:
            self.id = id
            data = Cache.hget(self.container, self.cache_key())
            if not data:
                raise DbException('object not found')

        if data is not None:
            deserialized = simplejson.loads(data)
            for key in deserialized:
                setattr(self, key, deserialized[key])
                if not key in self.serializable:
                    self.serializable.append(key)
        else:
            self.id = str(uuid.uuid1())
            self.creation_time = datetime.datetime.now()


    def cache_key(self):
        '''
        Returns the key which identifies object in cache
        '''
        return "%s:%s" % (self.container, self.id)


    def save(self, skip_lock=False):
        '''
        Store object in cache
        '''
        l = Cache.lock(self.container + ':' + ':lock')
        if not skip_lock:
            l.acquire()

        d = {}
        for field in self.serializable:
            d[field] = getattr(self, field, None)

        r = simplejson.dumps(d)
        Cache.hset(self.container, self.cache_key(), r)
        for key in self.keys:
            Cache.hset(self.container + ':' + key, self.cache_key(), getattr(self, key))

        if not skip_lock:
            l.release()

    def delete(self, skip_lock=False):
        '''
        Delete whole object from cache
        '''
        l = Cache.lock(self.container + ':' + ':lock')
        if not skip_lock:
            l.acquire()

        Cache.hdel(self.container, self.cache_key())
        for key in self.keys:
            Cache.hdel(self.container + ':' + key, self.cache_key())

        if not skip_lock:
            l.release()