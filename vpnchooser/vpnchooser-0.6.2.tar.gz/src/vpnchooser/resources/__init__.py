# -*- encoding: utf-8 -*-

from vpnchooser.applicaton import api

from .device import DeviceResource, DeviceListResource
from .vpn import VpnResource, VpnListResource
from .user import UserResource, UserListResource


api.add_resource(
    DeviceListResource,
    '/devices', '/devices/',
    endpoint='device_list'
)
api.add_resource(
    DeviceResource,
    '/devices/<int:device_id>',
    endpoint='device'
)
api.add_resource(
    VpnListResource,
    '/vpns', '/vpns/',
    endpoint='vpn_list')
api.add_resource(
    VpnResource,
    '/vpns/<int:vpn_id>',
    endpoint='vpn'
)
api.add_resource(
    UserListResource,
    '/users', '/users/',
    endpoint='user_list'
)
api.add_resource(
    UserResource,
    '/users/<string:user_name>',
    endpoint='user'
)
