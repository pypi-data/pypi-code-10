#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: utils.py
Version: 0.1
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2015-11-24
"""

import cherrypy
from dowser import Root


def launch_memory_usage_server(port=8080, show_trace=False):
    config = {
        'environment': 'embedded',
        'server.socket_port': port,
    }
    if show_trace:
        config.update({
            'global': {
                'request.show_tracebacks': True
            }}
        )
    cherrypy.tree.mount(Root())
    cherrypy.config.update(config)
    cherrypy.engine.start()
