import os
import logging
import logging.handlers

__author__ = 'umairghani'


class Logger:
    def __init__(self, dir, name):
        if not os.path.isdir(dir):
            os.mkdir(dir)
        self.logfile = os.path.join(dir, name)
        self.name = name
        self.logger = None
        self.__setup__()

    def __setup__(self):
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        consoleHandler = logging.handlers.RotatingFileHandler(self.logfile, mode='a', maxBytes=1024000, backupCount=10)
        consoleHandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        consoleHandler.setFormatter(formatter)
        self.logger.addHandler(consoleHandler)

    def get_logger(self):
        return self.logger


