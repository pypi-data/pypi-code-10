from __future__ import print_function

__doc__ = """
===============================================================================
Overview
===============================================================================

The mouse-record program is designed for the ease of recording and singling
out desired behavior of rodents, namely the events of interest in
reward-stimulus studies. Using these events as triggers (e.g., the press
of a lever), the program records the user-specified time before and after
a desired event. The generated H264 video files are saved into the desired
directory.

===============================================================================
API
===============================================================================
"""

__author__ = "Bailey Nozomu Hwa <hwab@janelia.hhmi.org"
__date__ = "$July 30, 2015 20:20:18 EDT$"

import argparse
import io
import datetime
import os


class Trigger(object):
    """
        Responsible for setting event trigger and waiting for updates.

        Notes:
            Relies on GPIO ports on the RaspberryPi for event notification.

        Attributes:
            port(int):                      GPIO port of trigger.
    """

    def __init__(self, port=27):
        """
            Function sets up GPIO port as argument.

            Args:
                port(Optional[int]):        GPIO port of trigger.
        """
        self.port = port

        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port, GPIO.IN, GPIO.PUD_UP)

    def wait(self):
        """
            Function sets initiation of trigger event.
        """

        import RPi.GPIO as GPIO
        GPIO.wait_for_edge(self.port, GPIO.FALLING)


def main(*argv):
    """
        Simple main function that performs event center recording.

        Args:
            argv(str):                      Arguments are stored as a list

        Notes:
            These are the parameters of the arguments.

            * folder(str):                  File directory
            * x(int):                       Time to recording before (seconds)
            * y(int):                       Time to record after (seconds)
    """

    # Time to record before and after as well as directory are stored here
    parser = argparse.ArgumentParser(
        description="seconds before and after lever is pressed."
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=27,
        help="GPIO port of trigger"
    )
    parser.add_argument(
        "before",
        type=int,
        help="seconds to record before."
    )
    parser.add_argument(
        "after",
        type=int,
        help="seconds to record after."
    )
    parser.add_argument(
        "folder",
        nargs='?',
        type=str,
        default=os.getcwd(),
        help="where to save the data (default is current working directory)."
    )
    args = parser.parse_args(argv[1:])

    folder = args.folder
    x = args.before
    y = args.after
    # z is the total number of seconds to be stored in the buffer
    z = x + y

    # sets up trigger event for the recordings, i.e., GPIO 27
    trigger = Trigger(args.port)

    import picamera
    with picamera.PiCamera(framerate=90) as camera:
        try:
            # Creates directory/folder if the desired directory is nonexistent
            if not os.path.exists(folder):
                os.makedirs(folder)
            stream = picamera.PiCameraCircularIO(camera, seconds=z)
            while True:
                # Up until now, the program defines the arguments and settings
                # for the Raspberry Pi camera and trigger event(GPIO 27)
                # The code below provides the recording protocol for the
                # stream, based on the initiation of the trigger event
                stream.seek(0)
                camera.start_recording(stream, format="h264", splitter_port=1)
                trigger.wait()
                camera.wait_recording(y, splitter_port=1)
                camera.stop_recording()

                for frame in stream.frames:
                    if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                        stream.seek(frame.position)
                        break
                # Gives the time specifications that you want, in
                # year-month-day_hour:minute:second:microsecond
                j = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
                # Responsible for saving and writing the stream
                # to a h264 video file
                with io.open(
                        os.path.join(
                            folder,
                            "mouse_press-" + str(j).replace(' ', '_') + ".h264"
                        ),
                        "wb"
                ) as output:
                    data = stream.read()
                    if not data:
                        break
                    output.write(data)
        except KeyboardInterrupt:
            print("Program is now ending session.")

    return 0
