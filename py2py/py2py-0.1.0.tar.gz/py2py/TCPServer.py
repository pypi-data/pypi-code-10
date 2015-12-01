import socketserver

class TCPServer(socketserver.TCPServer):
    '''A TCP Server which sends to soem event Handler on POST'''

    def __init__(self, location, tcp_handler, event_handler):
        super().__init__(location, tcp_handler)
        self.event_handler = event_handler
        self.can_serve = True

    def serve_forever(self):
        """Handle one request at a time until doomsday."""
        while self.can_serve:
            self.handle_request()

    def stop(self):
        """Stop serving"""
        self.can_serve = False

    def interpret(self, msg):
        """Send to event_handler"""
        self.event_handler.interpret(msg)
