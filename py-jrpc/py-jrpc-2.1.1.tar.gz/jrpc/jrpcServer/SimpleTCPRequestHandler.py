import BaseHTTPServer
import json
import urlparse

__author__ = 'umairghani'


class SimpleTCPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Base class for HTTP request handler
    """
    def do_GET(self):
        """
        Handle the HTTP GET request
        :return: Serve a GET request
        """
        url = urlparse.urlparse(self.path)
        method = url.path.split("/")[1]
        try:
            result = self.server._dispatch(method, url.params)
            response = self._dump(method, result)
            self._send(response)
        except TypeError, e:
            self.send_error(400, str(e))
        except NameError, e:
            self.send_error(405, str(e))
        except ValueError, e:
            self.send_error(500, str(e))

    def do_POST(self):
        """
        Handles the HTTP Post request
        :return:
        """
        if self.headers.has_key("content-length"):
            max_chunk_size = 10*1024*1024
            size_remaining = int(self.headers["content-length"])
            L = []
            while size_remaining:
                chunk_size = min(size_remaining, max_chunk_size)
                chunk = self.rfile.read(chunk_size)
                if not chunk:
                    break
                L.append(chunk)
                size_remaining -= len(L[-1])
            data = ''.join(L)
        else:
            self.send_error(411)

        try:
            method, params = self._load(data)
            #params = [params] if params else ""
            result = self.server._dispatch(method, params)
            response = self._dump(method, result)
            self._send(response)
        except ValueError, e:
            self.send_error(500, str(e))
        except NameError, e:
            self.send_error(405, str(e))

    def _send(self, data):
        """
        Writes data to the response
        :param data:
        :return: Nothing
        """
        self.send_response(200, str(data))
        self.send_header("Content-type", "application/json")
        self.send_header("Accept", "application/json")
        self.send_header("Content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _load(self, data):
        """
        Parses the data
        :param data:
        :return: key, value
        """
        r = json.loads(data)
        return r.items()[0]

    def _dump(self, method_name, data):
        """
        converts it to json
        :param data:
        :return: json object
        """
        result = {method_name: data}
        return json.dumps(result)

    def log_request(self, code='-', size='-'):
        """
        Logging function
        :param code:
        :param size:
        """
        if self.server.logging:
            BaseHTTPServer.BaseHTTPRequestHandler.log_request(self, code, size)
