from djwebsockets.server import WebSocketServer
from djwebsockets.mixins import BaseWSMixin, MixinFail
import djwebsockets as settings
import inspect


def Namespace(namespace):
    def socketplacer(clsitem):
        if WebSocketServer.NameSpaces.get(namespace) is None:
            WebSocketServer.NameSpaces.update({namespace:BaseWSClass})
            print("Websocket namespace \"{}\" registered for {}".format(settings.WEBSOCKET_BASE_URI+namespace, clsitem.__name__))
        return clsitem
    return socketplacer

