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

    def set_pre_action(self, pre_action_host, pre_action_port):
        """
        for 1st phase
        """
        self.pre_action_host = pre_action_host
        self.pre_action_port = pre_action_port
        self.pre_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pre_sock.connect((pre_action_host, pre_action_port))
        logger.info('[PRE] Connect to {} {}'.format(self.pre_action_host, self.pre_action_port))

    def send_pre_action_message(self, message=''):
        """
        for 1st phase
        """
        self.pre_sock.sendall(message)
        logger.info('[PRE] Send {} to {} {}'.format(message, self.pre_action_host, self.pre_action_port))

    def recv_pre_action_message(self, bufsize=1024):
        """
        for 1st phase
        """
        return self.pre_sock.recv(bufsize)

    def finish_pre_action(self):
        """
        for 1st phase
        """
        logger.info('[PRE] Close socket to {} {}'.format(self.pre_action_host, self.pre_action_port))
        self.pre_sock.close()

    def start(self):
        """
        for 2nd phase
        """
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
        """
        for 2nd phase
        """
        return self.conn.recv(bufsize)

    def sendall(self, data):
        """
        for 2nd phase
        """
        self.conn.sendall(data)
        logger.info('Send {} to {}'.format(data, self.conn_addr))

    def close(self):
        """
        for 2nd phase
        """
        logger.info('Close server of address: {}, port: {}'.format(self.addr, self.port))
        self.sock.close()


if __name__ == "__main__":
    # Testing controller
    import sys

    formatter = '%(levelname)s: %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)

    # create controller
    controller = PresentationApiController()
    # get controller's address
    controller_host = controller.get_addr()
    controller_port = controller.get_port()
    print('Controller runs on {} {}'.format(controller_host, controller_port))

    # First Phase
    print('\n# 1st phase\n')
    print('\rEnter host: '),
    pre_action_host = sys.stdin.readline().strip()
    print('\rEnter port: '),
    pre_action_port = int(sys.stdin.readline())

    # setup presentation server's host and port
    controller.set_pre_action(pre_action_host, pre_action_port)

    # for "format" method, brackets should use {{ or }} to escape.
    pre_msg = '{{"controller": {{"host": "{}", "port": {}}} }}'.format(controller_host, controller_port)
    # send message to presentation server
    controller.send_pre_action_message(pre_msg)

    # receive the message from presentation sever
    pre_received = controller.recv_pre_action_message()
    print('\nRecv: {}'.format(pre_received))

    # close socket
    controller.finish_pre_action()

    # Second Phase
    print('\n# 2nd phase\n')
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
