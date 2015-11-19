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

from coreinit.db.drivers.cache_interface import CacheInterface
from coreinit.service.mixins.avahi import AutoDiscoverMixin
from coreinit.utils.installer import *
from coreinit.utils.exceptions import *
import random

class Cache(AutoDiscoverMixin, CacheInterface):
    conn = None

    def configure(self):
        super(Cache, self).configure()
        self._autodiscover_configure()
        install_pip(['redis', 'simplejson'])

    def __init__(self):
        self.configure()
        endpoints = self._get_services('cache_redis')
        if len(endpoints) == 0:
            raise ConfigurationException('failed to find cache service')

        import redis
        self.conn = redis.Redis(endpoints[int(random.random() * len(endpoints))][0], socket_keepalive=1)

    def hset(self, name, key, value):
        return self.conn.hset(name, key, value)

    def hget(self, name, key):
        return self.conn.hget(name, key)

    def hdel(self, name, key):
        return self.conn.hdel(name, key)

    def hkeys(self, name):
        return self.conn.hkeys(name)

    def hvals(self, name):
        return self.conn.hvals(name)

    def keys(self):
        return self.conn.keys()

    def delete(self, name):
        return self.conn.delete(name)

    def lock(self, name):
        return self.conn.lock(name)