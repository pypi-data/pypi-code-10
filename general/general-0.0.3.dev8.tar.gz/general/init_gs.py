#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


from general import gs
log=gs.get_logger(__name__,debug=False)

from general.gs import cfg,types
PortType = types.Integer(1, 65535)

OPTS = [
    cfg.StrOpt('redis_server',
               default='localhost',
               help='redis server to connect  to '),
    cfg.Opt('redis_port',
            type=PortType,
            default=6379,
            help='redis port number to connect to'),
    cfg.StrOpt('mongo_server',
               default='localhost',
               help='mongo server to connect  to '),
    cfg.Opt('mongo_port',
            type=PortType,
            default=27017,
            help='mongo port number to connect to'),
    ]


gs.init(__file__,OPTS)

# log=gs.get_logger(__name__,debug=gs.CONF.debug)

log.debug("gs loaded, root is "+gs.CONF.root_package_name)
