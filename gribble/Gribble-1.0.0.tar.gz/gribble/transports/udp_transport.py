# -*- coding: utf-8 -*-
import socket

from gribble.transports.base_transport import BaseTransport


class UdpTransport(BaseTransport):

    def __init__(self, gribble_config, logger=None):
        super(UdpTransport, self).__init__(gribble_config, logger=logger)

        self._sock = socket.socket(socket.AF_INET,  # Internet
                                   socket.SOCK_DGRAM)  # UDP
        self._address = (gribble_config.get('udp_host'), gribble_config.get('udp_port'))

    def callback(self, filename, lines, **kwargs):
        timestamp = self.get_timestamp(**kwargs)
        if kwargs.get('timestamp', False):
            del kwargs['timestamp']

        for line in lines:
            self._sock.sendto(self.format(filename, line, timestamp, **kwargs), self._address)
