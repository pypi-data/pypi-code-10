# -*- encoding: utf-8 -*-

from flask import g

from vpnchooser.db import User


def current_user() -> User:
    return getattr(g, 'user', None)
