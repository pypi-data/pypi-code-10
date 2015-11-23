# -*- encoding: utf-8 -*-

import os
import hashlib

from passlib.hash import pbkdf2_sha512
from sqlalchemy.ext.hybrid import hybrid_property

from .database import db


class User(db.Model):
    """
    A user resource to be able to authenticate.
    """

    __tablename__ = 'user'

    name = db.Column(db.Unicode(255), primary_key=True)

    _password = db.Column('password', db.Unicode(512), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = pbkdf2_sha512.encrypt(password)

    def check(self, password: str) -> bool:
        """
        Checks the given password with the one stored
        in the database
        """
        return (
            pbkdf2_sha512.verify(password, self.password) or
            pbkdf2_sha512.verify(password,
                                 pbkdf2_sha512.encrypt(self.api_key))
        )

    is_admin = db.Column(db.Boolean, default=False,
                         server_default='false')

    _api_key = db.Column('api_key', db.Unicode(512), nullable=False)

    def generate_api_key(self):
        self._api_key = hashlib.new('sha512',
                                    os.urandom(512)).hexdigest()

    @hybrid_property
    def api_key(self):
        if self._api_key is None:
            self.generate_api_key()
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key

    @api_key.expression
    def api_key(cls):
        return cls._api_key
