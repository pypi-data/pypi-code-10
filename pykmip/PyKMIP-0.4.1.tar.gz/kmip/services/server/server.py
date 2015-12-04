# Copyright (c) 2015 The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import socket
import ssl
import sys


class KmipServer(object):
    """
    """

    def __init__(self, host=None, port=None, keyfile=None, certfile=None,
                 cert_reqs=None, ssl_version=None, ca_certs=None):
        self.logger = logging.getLogger('kmip.server')

        self._set_variables(host, port, keyfile, certfile, cert_reqs,
                            ssl_version, ca_certs)

#        handler = KMIPImpl()
#        self._processor = Processor(handler)

    def start(self):
        """
        """
        # Create a TCP stream socket and configure it for immediate reuse.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.socket.bind((self.host, self.port))
        except:
            self.logger.exception(
                "Server failed to bind socket handler to {0}:{1}".format(
                    self.host, self.port
                )
            )
            sys.exit(-1)
        else:
            self.logger.info(
                "Server successfully bound socket handler to {0}:{1}".format(
                    self.host, self.port
                )
            )

    def stop(self):
        """
        """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def server(self):
        """
        """
        self.socket.listen(1)
        while True:
            connection, address = self.socket.accept()
            connection = ssl.wrap_socket(
                connection,
                keyfile=self.keyfile,
                certfile=self.certfile,
                server_side=True,
                cert_reqs=self.cert_reqs,
                ssl_version=self.ssl_version,
                ca_certs=self.ca_certs,
                do_handshake_on_connect=True,
                suppress_ragged_eofs=True)

#            factory = KMIPProtocolFactory()
#            protocol = factory.getProtocol(connection)

#            try:
#                while True:
#                    self._processor.process(protocol, protocol)
#            except Exception as e:
#                self.logger.error('KMIPServer {0} {1}'.format(type(e), e))
#                connection.close()

    def _set_variables(self, host, port, keyfile, certfile, cert_reqs, ssl_version, ca_certs):
        self.host = host
        self.port = port

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
