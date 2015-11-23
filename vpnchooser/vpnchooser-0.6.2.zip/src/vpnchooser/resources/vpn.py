# -*- encoding: utf-8 -*-

from flask.ext.restful import (
    Resource,
    fields,
    marshal_with,
    abort,
    url_for
)
from flask.ext.restful.reqparse import RequestParser

from vpnchooser.helpers import (
    require_admin, require_login
)
from vpnchooser.helpers.fields import AbsoluteUrl
from vpnchooser.db import session, Vpn


parser = RequestParser()
parser.add_argument(
    'name', type=str,
    required=True,
    help='The name of the vpn.'
)
parser.add_argument(
    'description', type=str,
    required=True,
)
parser.add_argument(
    'table', type=str,
    required=True,
)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'table': fields.String,
    'self': AbsoluteUrl('vpn', data_func=lambda obj: {
        'vpn_id': obj.id
    }),
}


class AbstractVpnResource(Resource):
    """
    Abstract of the resource.
    """

    @staticmethod
    def update(vpn: Vpn) -> Vpn:
        args = parser.parse_args()
        vpn.name = args.name
        vpn.description = args.description
        vpn.table = args.table
        return vpn


class VpnResource(AbstractVpnResource):
    """
    The resource to access a vpn resource.
    """

    @staticmethod
    def _get_by_name(vpn_id: int) -> Vpn:
        return session.query(Vpn).filter(
            Vpn.id == vpn_id
        ).first()

    def _get_or_abort(self, vpn_id: int):
        vpn = self._get_by_name(vpn_id)
        if vpn is None:
            abort(404)
        else:
            pass
        return vpn

    @require_login
    @marshal_with(resource_fields)
    def get(self, vpn_id: int) -> Vpn:
        """
        Gets the VPN Resource.
        """
        return self._get_or_abort(vpn_id)

    @require_admin
    @marshal_with(resource_fields)
    def put(self, vpn_id: int) -> Vpn:
        """
        Updates the Vpn Resource with the
        name.
        """
        vpn = self._get_or_abort(vpn_id)
        self.update(vpn)
        session.commit()
        return vpn

    @require_admin
    def delete(self, vpn_id: int):
        """
        Deletes the resource with the given name.
        """
        vpn = self._get_or_abort(vpn_id)
        session.delete(vpn)
        session.commit()
        return '', 204


class VpnListResource(AbstractVpnResource):
    """
    List resource for the vpn.
    """

    @require_login
    @marshal_with(resource_fields)
    def get(self):
        return list(session.query(Vpn))

    @require_admin
    @marshal_with(resource_fields)
    def post(self) -> Vpn:
        """
        Creates the vpn with the given data.
        """
        vpn = Vpn()
        session.add(vpn)
        self.update(vpn)
        session.flush()
        session.commit()
        return vpn, 201, {
            'Location': url_for('vpn', vpn_id=vpn.id)
        }
