# -*- coding: utf-8 -*-

from zmq.eventloop import ioloop

ioloop.install()

from pyrocumulus.db import MongoConnection

connection = MongoConnection()
connection.connect()


VERSION = '0.11.1.1'
