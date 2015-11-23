from copy import deepcopy
from threading import Event, Lock, Thread

import bluetooth as bt

from constants import UUID
from receiver import Receiver


class Pi(Thread):
    def __init__(self):
        Thread.__init__(self)

        self._devices = {}
        self._lock_devices = Lock()

        self.server_sock = bt.BluetoothSocket(bt.RFCOMM)
        self.server_sock.bind(('', bt.PORT_ANY))
        self.server_sock.listen(1)
        self.done = None
        port = self.server_sock.getsockname()[1]

        bt.advertise_service(self.server_sock, 'SampleServer',
                             service_id=UUID,
                             service_classes=[UUID, bt.SERIAL_PORT_CLASS],
                             profiles=[bt.SERIAL_PORT_PROFILE])

        print('Waiting for connection on RFCOMM channel %d' % port)

    @property
    def devices(self):
        self._lock_devices.acquire()
        devs = deepcopy(self._devices)
        self._lock_devices.release()
        return devs

    def run(self):
        self.done = Event()
        while not self.done.isSet():
            print('Waiting for clients')
            client_sock, client_info = self.server_sock.accept()
            r = Receiver(self, client_sock, client_info)
            r.daemon = True
            r.start()

        self.server_sock.close()
        print('The server socket has been closed')

    def stop(self):
        try:
            self.done.set()
        except AttributeError:
            print('The server cannot be stopped. It is not running')
        else:
            print('The server has been stopped')

    def update_device(self, device, data):
        self._lock_devices.acquire()
        self._devices[device] = data
        self._lock_devices.release()


def main():
    p = Pi()
    p.start()
    try:
        raw_input('Press "enter" or "ctrl + c" to stop the server\n')
    except KeyboardInterrupt:
        print()
    finally:
        p.stop()


if __name__ == '__main__':
    main()
