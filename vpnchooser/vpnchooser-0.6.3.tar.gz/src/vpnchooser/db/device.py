# -*- encoding: utf-8 -*-

from vpnchooser.objects import Rule

from .database import db


class Device(db.Model):
    """
    A device in the network.
    """

    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)

    ip = db.Column(db.Unicode(255), nullable=False)

    name = db.Column(db.Unicode(255), nullable=False)

    type = db.Column(db.Unicode(255), nullable=True)

    vpn_id = db.Column(
        db.Integer,
        db.ForeignKey('vpn.id'),
        nullable=True
    )

    vpn = db.relationship(
        'Vpn',
        uselist=False,
        lazy=False,
        backref=db.backref('devices',
                           uselist=True,
                           lazy=True)
    )

    @property
    def rule(self) -> Rule:
        if self.vpn is None:
            return None

        rule = Rule()
        rule.ip = '{ip}/32'.format(
            ip=self.ip
        )
        rule.table = self.vpn.table
        return rule
