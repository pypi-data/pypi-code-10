#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry


from try1 import conf,cfg
from oslo_config import types
PortType = types.Integer(1, 65535)

print conf.bind_host


common_opts = [
    cfg.Opt('bind_port',
            type=PortType,
            default=9292,
            help='Port number to listen on.')
]

conf.register_opts(common_opts)



if __name__ == '__main__':
    pass


