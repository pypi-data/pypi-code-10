
import os
import logging

DEBUG = os.getenv('ZEROTEST_DEBUG', 'false').lower() == 'true'


def init_logging_config():
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        # disable requests log
        logging.getLogger("requests").setLevel(logging.WARNING)
