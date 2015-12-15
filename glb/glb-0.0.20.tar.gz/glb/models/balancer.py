# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glb.core.extensions import allocated_port
from .base import Model


class Balancer(Model):
    __prefix_key__ = 'balancers'
    __primary_key__ = 'name'

    def set_frontend(self, val):
        if val:
            if 'port' in val.keys():
                val.pop('port')
            self.frontend.update(val)
            return self.update(self.name, dict(frontend=self.frontend))

    def set_backends(self, val, action='update'):
        if getattr(self, 'backends', None) is None:
            self.backends = list()
        if val:
            if action == 'add':
                for backend in val:
                    if backend not in self.backends:
                        self.backends.append(backend)
            elif action == 'delete':
                for backend in self.backends:
                    if (backend['address'] == val['address'] and
                            backend['port'] == val['port']):
                        self.backends.remove(backend)
            elif action == 'delete_by_tag':
                self.backends = []
            else:
                self.backends = val
            return self.update(self.name, dict(backends=self.backends))

    def set_entrypoints(self, val, action='update'):
        if getattr(self, 'entrypoints', None) is None:
            self.entrypoints = list()
        if action == 'add':
            for entrypoint in val:
                if entrypoint not in self.entrypoints:
                    self.entrypoints.append(entrypoint)
        elif action == 'delete':
                if val['data'] in self._entrypoints:
                    self._entrypoints.remove(val['data'])
        elif action == 'delete_all':
            self._entrypoints = []
        else:
            self._entrypoints = val
        return self.update(self.name, dict(entrypoints=self.entrypoints))

    @classmethod
    def save_balancer(cls, val):
        val['frontend']['port'] = allocated_port()
        return cls.save(val)
