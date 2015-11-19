from coreinit.msg.queue_base import QueueBase
from coreinit.utils.installer import *
from coreinit.utils.exceptions import *
import socket

class Queue(QueueBase):
    s = None
    endpoint_socket = None
    address = None
    mode = None
    port = None

    def configure(self, mode, endpoint):
        super(Queue, self).configure(mode, endpoint)

        self.address, port = endpoint.split(':')
        self.port = int(port)
        self.mode = mode

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if mode == 'LISTEN':
            self.s.bind((self.address, self.port))
            self.s.listen(5)
        elif mode == 'CONNECT':
            self.endpoint_socket = self.s
        else:
            raise CoreException('queue_unknown_mode')

    def accept(self):
        self.endpoint_socket = self.s.accept()[0]
        return self


    def connect(self):
        self.endpoint_socket.conect((self.address, self.port))


    def close(self):
        self.endpoint_socket.close()


    def send(self, data):
        super(Queue, self).send(data)
        self.endpoint_socket.send(data)


    def recv(self, blocking=True):
        super(Queue, self).recv(blocking)
        if not blocking:
            raise CoreException('non blocking sockets are not supported')

        return self.endpoint_socket.recv(1024*1024)