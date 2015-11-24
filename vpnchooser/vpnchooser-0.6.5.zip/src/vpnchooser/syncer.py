# -*- encoding: utf-8 -*-

from vpnchooser.connection import Client
from vpnchooser.db import session, Device

from .applicaton import celery


class Syncer:
    """
    Handler to sync the current dataset
    to the rule set of the client.
    """

    def __init__(self):
        self.client = Client()

    def sync(self):
        return self.client.sync(self.rules)

    @property
    def rules(self):
        qry = session.query(Device).filter(Device.vpn_id != None)
        return [
            item.rule
            for item in qry
        ]


@celery.task(name='vpnchooser.sync')
def sync():
    """
    Synchronizes the current dataset from the database
    with the ip rule set on the router system.
    """
    syncer = Syncer()
    return syncer.sync()
