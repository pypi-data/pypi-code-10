import SocketServer

from SimpleTCPDispatcher import SimpleTCPDispatcher
from SimpleTCPRequestHandler import SimpleTCPRequestHandler

__author__ = 'umairghani'


class SimpleTCPServer(SocketServer.TCPServer, SimpleTCPDispatcher):
    """
    Simple TCP Server
    """

    allow_reuse_address = True

    def __init__(self, address, request_handler=SimpleTCPRequestHandler,
                 logging=True, bind_and_activate=True):
        """
        :constructor:
        :param address:
        :param request_handler (optional):
        :param bind_and_activate (optional):
        """
        self.logging = logging
        SimpleTCPDispatcher.__init__(self)
        SocketServer.TCPServer.__init__(self, address, request_handler, bind_and_activate)
