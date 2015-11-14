import logging
from subprocess import check_call, check_output
import time

from serial import Serial


SERVICE_PATH = '/usr/sbin/service'
STATE_CHECK_INTERVAL = 30


logger = logging.getLogger(__name__)


class SerialButtonManager(object):
    def __init__(self, device, service):
        self.device = Serial(device)
        self.service_name = service

    @property
    def service_is_running(self):
        output = check_output(
            [
                SERVICE_PATH,
                self.service_name,
                'status',
            ]
        )
        output = output.strip()
        logger.debug('Service status result: %s', output)

        if 'stop' in output:
            logger.debug('Service is not running.')
            return False
        elif 'start' in output:
            logger.debug('Service is running.')
            return True

        raise RuntimeError('Unable to get service status: "%s"' % output)

    @property
    def button_is_pressed(self):
        return self.device.getCD()

    def start_service(self):
        check_call(
            [
                SERVICE_PATH,
                self.service_name,
                'start',
            ]
        )

    def stop_service(self):
        check_call(
            [
                SERVICE_PATH,
                self.service_name,
                'stop',
            ]
        )

    def _resolve_state_mismatch(self):
        running = self.service_is_running
        pressed = self.button_is_pressed

        if pressed and not running:
            logger.warning(
                "State mismatch detected; button was pressed, but "
                "service was not running; starting service."
            )
            self.start_service()
        elif not pressed and running:
            logger.warning(
                "State mismatch detected; button was not pressed, but "
                "service was running; stopping service."
            )
            self.stop_service()

    def run(self):
        self._resolve_state_mismatch()
        last_checked_state = time.time()

        last_state = self.button_is_pressed
        while True:
            pressed = self.button_is_pressed
            if pressed != last_state:
                last_checked_state = time.time()

                if pressed:
                    logger.info(
                        "Button press detected: starting service."
                    )
                    self.start_service()
                else:
                    logger.info(
                        "Button unpress detected: starting service."
                    )
                    self.stop_service()
            elif last_checked_state + STATE_CHECK_INTERVAL < time.time():
                last_checked_state = time.time()
                self._resolve_state_mismatch()

            last_state = pressed
            time.sleep(0.5)
