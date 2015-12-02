from ..sig import *

class LocalCarrier(Carrier):
    def __init__(self):
        Carrier.__init__(self)
        self.connected_carrier = None

    def connect(self, carrier):
        self.connected_carrier = carrier
        carrier.connected_carrier = self

        # connect callbacks
        self.handle_client_connected(id(self))
        carrier.handle_client_connected(id(carrier))

    def disconnect():
        if self.connected_carrier is None:
            return

        carrier = self.connected_carrier
        self.connected_carrier = None
        carrier.connected_carrier = None

        # disconnect callbacks
        self.handle_client_disconnected(id(carrier))
        carrier.handle_client_disconnected(id(self))

    def RX(self, clientid, data):
        # unpack
        message = self.unpack(data)
        if message is None:
            return None

        # transmit unpacked message
        reply = self.handleRX(clientid, message)
        return reply

    def handleTX(self, clientid, data):
        
        # pack
        message = self.pack(data)
        if message is None:
            return

        # pipe message
        reply = self.connected_carrier.RX(id(self.connected_carrier), message)
        return reply
