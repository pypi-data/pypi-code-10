from urlparse import urlparse
import socket


class Sender(object):

    @classmethod
    def from_components(cls, components):
        raise cls(**components)

    def __init__(self, sendable):
        self.sendable = sendable
        self.transport = Transport.from_sendable(sendable)

    def __enter__(self):
        self.transport.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.transport.close()

    def session(self):
        return SenderSession(self)

    def send(self, data):
        self.transport.send(data)


class SenderSession(object):
    def __init__(self, sender):
        self.sender = sender

    def __enter__(self):
        return self.sender.__enter__()

    def __exit__(self, *args):
        return self.sender.__exit__(*args)


class Transport(object):
    TRANSPORTS = []

    @staticmethod
    def register(transport):
        Transport.TRANSPORTS.append(transport)

    @staticmethod
    def from_sendable(sendable):
        components = urlparse(sendable)
        transports = [t for t in Transport.TRANSPORTS if t.SCHEME == components.scheme]

        if not len(transports):
            raise Exception('Expected at least one matching transport')
        return transports.pop(0).from_components(components)

    @classmethod
    def from_components(cls, components):
        props = ['username', 'password', 'hostname', 'port']
        components_dict = dict([(k, getattr(components, k)) for k in props], **components._asdict())

        return cls(**components_dict)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def open(self):
        raise NotImplementedError('Transport missing open method')

    def close(self):
        raise NotImplementedError('Transport missing close method')

    def send(self, data):
        raise NotImplementedError('Transport missing send method')


class SocketTransport(Transport):

    @classmethod
    def __init__(cls, hostname=None, port=None, **kwargs):
        cls.address = (hostname, port)
        cls.socket = socket.socket(socket.AF_INET, cls.SOCKET_TYPE)

    def open(self):
        self.socket.connect(self.address)

    def close(self):
        self.socket.close()

    def send(self, data):
        sent = self.socket.send(data)
        if sent == 0:
            raise RuntimeError('unable to send to socket')


@Transport.register
class UdpTransport(SocketTransport):
    SCHEME = 'udp'
    SOCKET_TYPE = socket.SOCK_DGRAM


@Transport.register
class TcpTransport(SocketTransport):
    SCHEME = 'tcp'
    SOCKET_TYPE = socket.SOCK_STREAM
