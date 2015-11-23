# -*- encoding: utf-8 -*-

from flask.ext.restful import (
    Resource,
    fields,
    marshal_with,
    abort,
    url_for
)
from flask.ext.restful.reqparse import RequestParser

from vpnchooser.syncer import sync
from vpnchooser.helpers import (
    require_login,
    id_from_url
)
from vpnchooser.helpers.fields import AbsoluteUrl, NullableAbsoluteUrl
from vpnchooser.db import session, Device, Vpn


parser = RequestParser()
parser.add_argument(
    'ip', type=str,
    required=True,
)
parser.add_argument(
    'name', type=str,
    required=True,
)
parser.add_argument(
    'type', type=str,
    required=False,
)
parser.add_argument(
    'vpn', type=str,
    required=False
)

resource_fields = {
    'id': fields.Integer,
    'ip': fields.String,
    'name': fields.String,
    'type': fields.String,
    'vpn': NullableAbsoluteUrl('vpn', data_func=lambda obj: {
        'vpn_id': obj.vpn_id
    }),
    'self': AbsoluteUrl('device', data_func=lambda obj: {
        'device_id': obj.id
    }),
}


class AbstractDeviceResource(Resource):
    """
    Abstract of the resource.
    """

    @staticmethod
    def _update_vpn(args, device: Device) -> Device:
        orig_vpn = device.vpn
        if args.vpn:
            try:
                vpn_id = id_from_url(args.vpn, 'vpn_id')
                device.vpn = session.query(Vpn).filter(
                    Vpn.id == vpn_id
                ).first()
            except ValueError:
                device.vpn = None
        else:
            device.vpn = None

        if orig_vpn != device.vpn:
            sync.delay()
        return device

    def update(self, device: Device) -> Device:
        args = parser.parse_args()
        device.ip = args.ip
        device.name = args.name
        device.type = args.type
        self._update_vpn(args, device)
        return device


class DeviceResource(AbstractDeviceResource):
    """
    The resource to access a device resource.
    """

    @staticmethod
    def _get_by_id(device_id: int) -> Device:
        return session.query(Device).filter(
            Device.id == device_id
        ).first()

    def _get_or_abort(self, device_id: int):
        device = self._get_by_id(device_id)
        if device is None:
            abort(404)
        else:
            pass
        return device

    @require_login
    @marshal_with(resource_fields)
    def get(self, device_id: int) -> Device:
        """
        Gets the Device Resource.
        """
        return self._get_or_abort(device_id)

    @require_login
    @marshal_with(resource_fields)
    def put(self, device_id: int) -> Device:
        """
        Updates the Device Resource with the
        name.
        """
        device = self._get_or_abort(device_id)
        self.update(device)
        session.commit()
        session.add(device)
        return device

    @require_login
    def delete(self, device_id: int):
        """
        Deletes the resource with the given name.
        """
        device = self._get_or_abort(device_id)
        session.delete(device)
        session.commit()
        return '', 204


class DeviceListResource(AbstractDeviceResource):
    """
    List resource for the device.
    """

    @require_login
    @marshal_with(resource_fields)
    def get(self):
        devices = list(session.query(Device))
        return devices

    @require_login
    @marshal_with(resource_fields)
    def post(self) -> Device:
        device = Device()
        session.add(device)
        self.update(device)
        session.flush()
        session.commit()
        return device, 201, {
            'Location': url_for('device', device_id=device.id)
        }
