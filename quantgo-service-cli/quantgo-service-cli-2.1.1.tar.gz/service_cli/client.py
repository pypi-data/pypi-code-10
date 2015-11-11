from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
# ======================= QuantGo Copyright Notice ============================
# Copyright 2013 QuantGo, LLC.  All rights reserved.
# Permission to use solely inside a QuantGo Virtual Quant Lab
# Written By: Nikolay
# Date: 12-12.2013
# ======================= QuantGo Copyright Notice ============================

import logging
import socket
from . import config

BUFF_SIZE = 1024 * 1024
GREETING = None
GREETING_RESPONSE = 'OK'
#SOCKET_TIMEOUT = 5
SOCKET_TIMEOUT = None


class SRClientError(Exception):
    pass


class ConnectionError(SRClientError):
    pass


class SRClient(object):
    def __init__(self, host=config.HOST, port=config.PORT, buff_size=BUFF_SIZE, stdout=None):
        logging.debug('Initializing SRClient with params host=%s, port=%s',
                      host, port)
        self.host = host
        self.port = port
        self.buff_size = buff_size
        self.sock = None
        self.data = []
        self.received = 0
        self.stdout = stdout

    def connect(self):
        self.sock = socket.create_connection((self.host, self.port))
        self.sock.settimeout(SOCKET_TIMEOUT)

    def close(self):
        self.sock.close()

    def _handshake(self):
        if GREETING is not None:
            self.sock.send(b'{0}\n'.format(GREETING))
            resp = self.sock.recv(512).strip()
            if not resp == GREETING_RESPONSE:
                raise SRClientError('Unable to connect to quantgo-service host.')

    def send(self, data):
        self.sock.send(data.encode('utf-8'))
        self.sock.send(b'\n')

    def read_response(self):
        res = ''
        while True:
            data = self.sock.recv(1).decode('utf-8')
            if data == '\n':
                break
            res = res + data
        return res

    def receive(self):
        self.data = []
        while True:
            try:
                data = self.sock.recv(self.buff_size)
            except socket.timeout:
                data = None
            if not data:
                break

            self.received += len(data)

            if self.stdout:
                self.stdout.write(data)
            else:
                self.data.append(data.strip())

        # If self.stdout is defined, just finish, all data was already printed
        # to stdout.
        if self.stdout:
            return

        return ''.join(self.data)

    def __enter__(self):
        self.connect()
        self._handshake()
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.sock.close()
        if ex_type is not None:
            return False


if __name__ == '__main__':
    pass
