import socket, sys
from py2py.TCPServer import TCPServer
from py2py.HttpServer import HttpServer

class Listener(object):
    '''
    Http Server parent class; responsible for creating, binding, and listening
    '''

    def __init__(self, event_handler=None):
        self.handler_class = HttpServer
        self.server_class = TCPServer
        self.event_handler = event_handler

    def launch(self, port):
        '''
        Daemonized; Create and bind a socket on the location and port
        '''
        httpd = None
        try:
            self.server_class.allow_reuse_address = True
            httpd = self.server_class(("", port), self.handler_class, self)
            httpd.serve_forever()

        # No dice. Kill the process.
        except socket.error as msg:
            print('ERROR: Unable to bind socket: {0}'.format(msg))

        # Try to kill httpd
        if hasattr(httpd,'kill'):
            httpd.kill()


    def interpret(self, message):
        '''
        Received a message from the TCP Server, so relay it
        '''

        # Plaintext
        self.notify(message)

    def notify(self, message):
        '''Notify Event Handler'''
        if self.event_handler is not None:
            self.event_handler.handle_message(message)
            return

        # Prints only if there is no event handler
        print(message)
