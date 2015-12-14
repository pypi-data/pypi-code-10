#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from glb.settings import Config


def parse(data):
    if not data:
        data = list()
    upstreams = list()
    servers = list()
    ssl_files = set()
    for balancer in data:
        def parse_upstream():
            names = balancer.name.split("_")
            if len(names) > 2:
                names = names[:-1]
            names.append(Config.GLB_URL)
            upstream_name = '.'.join(names)
            servs = ["%s:%s" % (backend['address'], backend['port'])
                     for backend in balancer.backends]
            return dict(name=upstream_name,
                        servers=servs)
        upstreams.append(parse_upstream())

        def parse_servers():
            listens = list()
            server_names = list()
            port = balancer.frontend['port']
            protocol = balancer.frontend['protocol']
            is_ssl = True if protocol == 'ssl' else False
            listens.append(dict(port=port, is_ssl=is_ssl))
            for entrypoint in getattr(balancer, 'entrypoints', []):
                server_names.append(entrypoint['domain'])
                port = entrypoint['port']
                is_ssl = True if entrypoint['protocol'] in ['ssl', 'https'] else False
                listens.append(dict(port=port, is_ssl=is_ssl))
            return dict(listens=listens,
                        server_names=server_names)
        servers.append(parse_servers())
    upstreams.sort(key=lambda ups: ups['name'])
    return upstreams, servers, list(ssl_files)
