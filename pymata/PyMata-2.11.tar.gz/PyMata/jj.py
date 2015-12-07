import threading
import time

import serial


class PyMataSerial(threading.Thread):
    """
     This class manages the serial port for Arduino serial communications
    """

    def __init__(self, port_id, command_deque):
        """
        Constructor:
        @param command_deque: A reference to the deque shared with the _command_handler
        """
        self.port_id = port_id
        self.command_deque = command_deque

        threading.Thread.__init__(self)
        self.daemon = True
        self.arduino = serial.Serial(self.port_id, self.baud_rate,
                                     timeout=int(self.timeout), writeTimeout=0)

        self.stop_event = threading.Event()

    def is_stopped(self):
        return self.stop_event.is_set()

    def close(self):
        """
            Close the serial port
            return: None
        """
        try:
            self.arduino.close()
        except OSError:
            pass

    def run(self):
        """
        This method continually runs. If an incoming character is available on the serial port
        it is read and placed on the _command_deque
        @return: Never Returns
        """
        while not self.is_stopped():
            # we can get an OSError: [Errno9] Bad file descriptor when shutting down
            # just ignore it
            try:
                if self.arduino.inWaiting():
                    c = self.arduino.read()
                    self.command_deque.append(ord(c))
                else:
                    time.sleep(.1)
            except OSError:
                pass
        self.close()
