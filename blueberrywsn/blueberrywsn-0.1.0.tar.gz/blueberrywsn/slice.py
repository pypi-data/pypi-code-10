from threading import Event, Thread

import bluetooth as bt

from constants import UUID
from sensor import Sensor


INTERVAL = 1


class Slice(Thread):
    def __init__(self, local=False, interval=INTERVAL):
        Thread.__init__(self)
        self.done = None
        self.interval = interval
        self.local = local
        self.sensor = Sensor()

    def run(self):
        self.done = Event()
        while not self.done.wait(self.interval):
            info = self.sensor.read()
            if info:
                if self.local:
                    print info
                else:
                    self.send(info)
            else:
                print('The sensor could not be read')

    def send(self, info):
        # search for the server service
        service_matches = bt.find_service(uuid=UUID)

        if not service_matches:
            print('The server could not be found')

        first_match = service_matches[0]
        port = first_match['port']
        name = first_match['name']
        host = first_match['host']

        print('Attempting to connect to \'%s\' on %s' % (name, host))

        # Create the client socket
        sock = bt.BluetoothSocket(bt.RFCOMM)
        sock.connect((host, port))
        print('The connection has been accepted by the server')

        sock.send(str(info))
        print('The information has been sent')

        sock.close()
        print('The client socket has been closed')

    def stop(self):
        try:
            self.done.set()
        except AttributeError:
            print('The client cannot be stopped. It is not running')
        else:
            print('The client has been stopped')


def main():
    s = Slice()
    s.start()
    try:
        raw_input('Press "enter" or "ctrl + c" to stop the client\n')
    except KeyboardInterrupt:
        print()
    finally:
        s.stop()


if __name__ == '__main__':
    main()
