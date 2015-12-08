# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.errors import notfounderror
from glb.models.balancer import Balancer as BalancerModel


class BalancerBalancerNameEntrypoints(Resource):

    def get(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        if balancer:
            return balancer.entrypoints, 200, None
        else:
            return notfounderror()

    def post(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        if balancer:
            res = balancer.set_entrypoints(g.json, 'add')
            return res, 201, None
        else:
            return notfounderror()

    def put(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        if balancer:
            res = balancer.set_entrypoints(g.json, 'update')
            return res, 200, None
        else:
            return notfounderror()

    def delete(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        if balancer:
            domain = g.args.get('domain', '')
            port = g.args.get('port', 0)
            protocol = g.args.get('protocol', None)
            del_type = g.args.get('del_type', 'one')
            val = {}
            if del_type == 'all':
                action = 'delete_all'
            else:
                if domain and port and protocol:
                    val = dict(domain=domain,
                               port=port,
                               protocol=protocol)
                    action = 'delete'
            res = balancer.set_entrypoints(val, action)
            return res, 200, None
        else:
            return notfounderror()
