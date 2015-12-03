# -*- coding: utf-8 -*-


__author__ = "Robert Wikman <rbw@vault13.org>"

from clapi import Client


class CLAPI(object):
    def __init__(self, app=None):
        self.app = app
        self.clapi = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.clapi = Client(app.config['CLAPI_USERNAME'],
                            app.config['CLAPI_PASSWORD'],
                            app.config['CLAPI_PATH'],
                            app.config['CLAPI_DEBUG'])

    def __getattr__(self, name):
        return getattr(self.clapi, name)
