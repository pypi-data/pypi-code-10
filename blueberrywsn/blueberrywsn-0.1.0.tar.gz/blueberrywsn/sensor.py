from serial import Serial


PORT = '/dev/ttyACM0'
RATE = 9600


class Sensor:
    def __init__(self, port=PORT, rate=RATE):
        self.serial = None
        try:
            self.serial = Serial(port, rate)
        except OSError:
            print('The sensor reader cannot be found at %s' % port)

    def read(self):
        try:
            return self.serial.readline().strip()
        except AttributeError:
            return None
