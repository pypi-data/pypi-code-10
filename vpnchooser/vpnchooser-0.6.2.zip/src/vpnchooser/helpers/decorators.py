# -*- encoding: utf-8 -*-

from functools import wraps

from flask import request, Response, g

from vpnchooser.db import session, User
from .auth import current_user


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        # {'WWW-Authenticate': 'Basic realm="Login Required"'}
        {}
    )


def require_login(func):
    """
    Function wrapper to signalize that a login is required.
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        user = session.query(User).filter(
            User.name == auth.username
        ).first()
        if user and user.check(auth.password):
            g.user = user
            return func(*args, **kwargs)
        else:
            return authenticate()

    return decorated


def require_admin(func):
    """
    Requires an admin user to access this resource.
    """

    @wraps(func)
    @require_login
    def decorated(*args, **kwargs):
        user = current_user()
        if user and user.is_admin:
            return func(*args, **kwargs)
        else:
            return Response(
                'Forbidden', 403
            )

    return decorated
