import sys

# Load the correct servers
if sys.version_info[:2][0] >= 3:

    # Python 3 (Preferred)
    from py2py.python3.HttpServer import HttpServer
    from py2py.python3.TCPServer import TCPServer

else:
    # Python 2
    from py2py.python2.HttpServer import HttpServer
    from py2py.python2.TCPServer import TCPServer

from py2py.Listener import Listener
from py2py.Sender import Sender

__all__ = ["HttpServer", "TCPServer", "Listener", "Sender"]
