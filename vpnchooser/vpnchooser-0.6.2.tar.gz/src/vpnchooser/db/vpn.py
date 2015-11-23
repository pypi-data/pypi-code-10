# -*- encoding: utf-8 -*-

from .database import db


class Vpn(db.Model):
    """
    A vpn which is configured to a specific
    table rule.
    """

    __tablename__ = 'vpn'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255), nullable=False)

    description = db.Column(db.Unicode(255), nullable=False)

    table = db.Column(db.Unicode(255), nullable=False)
