import BaseHTTPServer, json

class HttpServer(BaseHTTPServer.BaseHTTPRequestHandler):
    """py2py HttpServer, handles POST messages"""

    def log_message(self, format, *args):
        """Overridden to keep quiet"""
        pass

    def do_POST(self):
        '''
        Actually handles the receipt of messages on the socket. This is its own
        method in case you want to extend it and add a blacklist or something
        like that.
        '''
        self.accept_POST()

    def accept_POST(self):
        """
        Accept the POST and interpret the post data
        """
        # Get the data
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)
        self.send_response(200, "OK")
        self.end_headers()

        # Now, interpret
        self.server.interpret(post_data)
