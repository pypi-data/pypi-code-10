import threading
import socket
import SocketServer


class ControllerTCPHandler(SocketServer.BaseRequestHandler):

    def set_response(self, response):
        self.response = response

    def handle(self):
        self.request.sendall('TEST')
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())
        self.request.sendall(self.response)


class PresentationApiController():

    def __init__(self, response_list):
        self.response_list = response_list
        
        # create TCP server
        self.server = SocketServer.TCPServer(('localhost', 0), ControllerTCPHandler)
        self.addr, self.port = self.server.socket.getsockname()
        print('Run server [{}], port [{}]'.format(self.addr, self.port))

        self.thread = threading.Thread(target=self.server.serve_forever())
        self.thread.start()

    def get_response_list(self):
        return self.response_list

    def get_addr(self):
        return self.addr

    def get_port(self):
        return self.port

    def shutdown(self):
        self.server.shutdown()

    def sendall(self, data):
        self.server.socket.sendall(data)


if __name__ == "__main__":
    print('Interrupt the Server with Crtl-C')
    PresentationApiController()
