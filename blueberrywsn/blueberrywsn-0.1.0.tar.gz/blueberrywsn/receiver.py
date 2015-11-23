from threading import Thread


class Receiver(Thread):
    def __init__(self, pi, client_sock, client_info):
        Thread.__init__(self)
        self.pi = pi
        self.client_sock = client_sock
        self.client_info = client_info

    def run(self):
        print('A new connection has been accepted from %s' % self.client_info)

        try:
            while True:
                data = self.client_sock.recv(1024)
                if len(data) == 0:
                    break
                print('Information received: %s' % data)
                self.pi.update_device(self.client_info[0], data)
        except IOError:
            pass

        print('Number of clients on the network: %d' % str(len(self.pi.devices)))

        self.client_sock.close()
        print('The client socket has been closed')
