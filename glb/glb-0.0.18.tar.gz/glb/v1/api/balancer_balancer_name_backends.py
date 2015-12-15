# -*- coding: utf-8 -*-
from flask import g

from . import Resource
from glb.core.errors import notfounderror
from glb.models.balancer import Balancer as BalancerModel


class BalancerBalancerNameBackends(Resource):

    def get(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        if balancer:
            return balancer.backends, 200, None
        else:
            return notfounderror()

    def post(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        if balancer:
            res = balancer.set_backends(g.json, 'add')
            return res, 201, None
        else:
            return notfounderror()

    def put(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        if balancer:
            res = balancer.set_backends(g.json, 'update')
            return res, 200, None
        else:
            return notfounderror

    def delete(self, balancer_name):
        balancer = BalancerModel.retrieve(balancer_name)
        print 'ssss'
        if balancer:
            address = g.args.get('address', '')
            port = int(g.args.get('port', 0))
            val = {}
            if g.args.get('tag', None) is None:
                action = 'delete'
                val = dict(address=address,
                           port=port)
            else:
                action = 'delete_by_tag'
            res = balancer.set_backends(val, action)
            return res, 200, None
        else:
            return notfounderror
