#!/usr/bin/env python

"""
dump HTTP requests
"""

# imports
import argparse
import os
import sys
import time
from wsgiref import simple_server
from webob import Request, Response

# module globals
__all__ = ['RequestDumpster']

class RequestDumpster(object):
    """WSGI interface to dump HTTP requests"""

    def __init__(self, directory=None):
        if directory is not None and not os.path.isdir(directory):
            raise Exception("Not a directory")
        self.directory = directory

    def __call__(self, environ, start_response):
        """WSGI"""

        request = Request(environ)
        lines = ["{REQUEST_METHOD} {PATH_INFO} {SERVER_PROTOCOL}".format(PATH_INFO=request.path_qs,
                                                                        REQUEST_METHOD=request.method,
                                                                        SERVER_PROTOCOL=request.environ['SERVER_PROTOCOL'])]
        lines.extend(['{0}: {1}'.format(*header)
                      for header in request.headers.items()])
        lines.append('')
        lines.append(request.body)
        body = '\r\n'.join(lines) + '\r\n'

        response = Response(content_type='text/plain',
                            body=body)
        return response(environ, start_response)

def main(args=sys.argv[1:]):
    """CLI"""

    # parse command line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port', dest='port',
                        type=int, default=9555,
                        help="port to serve on")
    parser.add_argument('-d', '--directory', dest='directory',
                        help="directory to output requests to")
    options = parser.parse_args()

    # instantiate WSGI app
    app = RequestDumpster(directory=options.directory)

    # construct url
    url = 'http://localhost:{port}/'.format(port=options.port)

    # serve some web
    host = '127.0.0.1'
    server = simple_server.make_server(host=host,
                                       port=options.port,
                                       app=app)
    print url
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
