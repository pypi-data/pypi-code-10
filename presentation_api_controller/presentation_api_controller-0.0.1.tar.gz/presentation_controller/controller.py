#!/usr/bin/env python

import socket
import logging

logger = logging.getLogger(__name__)


class PresentationApiController(object):

    def __init__(self):
        """
        Start socket, listen for connection, accept connection.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 0))
        self.addr, self.port = self.sock.getsockname()
        logger.info('Run server on address: {}, port: {}'.format(self.addr, self.port))

    def start(self):
        self.sock.listen(1)
        self.conn, (self.conn_addr, self.conn_port) = self.sock.accept()
        logger.info('Connected by {} {}'.format(self.conn_addr, self.conn_port))

    def get_addr(self):
        return self.addr

    def get_port(self):
        return self.port

    def get_socket(self):
        return self.sock
    
    def get_conn_addr(self):
        return self.conn_addr

    def get_conn_port(self):
        return self.conn_port

    def recv(self, bufsize=1024):
        return self.conn.recv(bufsize)

    def sendall(self, data):
        self.conn.sendall(data)

    def close(self):
        logger.info('Close server of address: {}, port: {}'.format(self.addr, self.port))
        self.sock.close()


if __name__ == "__main__":
    # Testing controller
    formatter = '%(levelname)s: %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)

    # create controller
    controller = PresentationApiController()

    # get controller's address
    controller_host = controller.get_addr()
    controller_port = controller.get_port()
    print('Controller runs on {} {}'.format(controller_host, controller_port))

    # start listen
    controller.start()

    # controller send message to client
    msg = 'This is Controller\'s first message.'
    controller.sendall(msg)
    print('Send: {}'.format(msg))

    # controller receive data
    controller_received = controller.recv(1024)
    print('Recv: {}'.format(controller_received))

    # controller send message to client
    msg = 'I will die. Bye bye.'
    controller.sendall(msg)
    print('Send: {}'.format(msg))

    # close
    controller.close()
