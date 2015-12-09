"""
Helpers module.

Contains helper classes for tests.
"""

import SocketServer
import SimpleHTTPServer
from Queue import Queue

SocketServer.TCPServer.allow_reuse_address = True


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """ Threaded TCP server """
    pass


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    """ Threaded UDP server """
    pass


def setup_tcp_server(queue):
    import SocketServer
    import threading

    from .helpers import ThreadedTCPServer

    class LineHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            """ Handle a request """
            _buffer = ""

            while 1:
                data = self.request.recv(1024)
                if len(data) < 1:
                    break
                _buffer += data

            for line in _buffer.splitlines():
                queue.put(line)

    server = ThreadedTCPServer(("localhost", 2013), LineHandler)
    server.thread = threading.Thread(target=server.serve_forever)
    server.thread.daemon = True
    server.thread.start()

    return server
