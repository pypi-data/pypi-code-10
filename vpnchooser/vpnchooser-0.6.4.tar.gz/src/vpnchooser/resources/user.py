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
    require_admin, require_login, current_user
)
from vpnchooser.helpers.fields import AbsoluteUrl
from vpnchooser.db import session, User


parser = RequestParser()
parser.add_argument(
    'name', type=str,
    required=False,
)
parser.add_argument(
    'password', type=str,
    required=False,
)
parser.add_argument(
    'is_admin', type=bool,
    required=False,
)


resource_fields = {
    'name': fields.String,
    'is_admin': fields.Boolean,
    'api_key': fields.String,
    'self': AbsoluteUrl('user', data_func=lambda obj: {
        'user_name': obj.name
    }),
}


class AbstractUserResource(Resource):
    """
    Abstract of the resource.
    """

    @staticmethod
    def _get_by_username(user_name: str) -> User:
        return session.query(User).filter(
            User.name == user_name
        ).first()

    @staticmethod
    def update(user: User) -> User:
        args = parser.parse_args()
        if not user.name and args.name:
            user.name = args.name
        if current_user().is_admin and args.is_admin is not None:
            user.is_admin = args.is_admin
        if args.password:
            user.password = args.password
            user.generate_api_key()
        return user


class UserResource(AbstractUserResource):
    """
    The resource to access a user resource.
    """

    def _get_or_abort(self, user_name: str):
        user = self._get_by_username(user_name)
        if user is None:
            abort(404)
        else:
            pass
        return user

    @require_login
    @marshal_with(resource_fields)
    def get(self, user_name: str) -> User:
        """
        Gets the User Resource.
        """
        user = current_user()
        if user.is_admin or user.name == user_name:
            return self._get_or_abort(user_name)
        else:
            abort(403)

    @require_login
    @marshal_with(resource_fields)
    def put(self, user_name: str) -> User:
        """
        Updates the User Resource with the
        name.
        """
        current = current_user()
        if current.name == user_name or current.is_admin:
            user = self._get_or_abort(user_name)
            self.update(user)
            session.commit()
            session.add(user)
            return user
        else:
            abort(403)

    @require_admin
    def delete(self, user_name: str):
        """
        Deletes the resource with the given name.
        """
        user = self._get_or_abort(user_name)
        session.delete(user)
        session.commit()
        return '', 204


class UserListResource(AbstractUserResource):
    """
    List resource for the user.
    """

    @require_login
    @marshal_with(resource_fields)
    def get(self):
        user = current_user()
        query = session.query(User)
        if not user.is_admin:
            query = query.filter(User.name == user.name)
        return list(query)

    @require_admin
    @marshal_with(resource_fields)
    def post(self) -> User:
        args = parser.parse_args()
        user = self._get_by_username(args.name)
        if user is not None:
            abort(409, message='User already exists')
        user = User()
        self.update(user)
        session.add(user)
        session.commit()
        return user, 201, {
            'Location': url_for('user', user_name=user.name)
        }
