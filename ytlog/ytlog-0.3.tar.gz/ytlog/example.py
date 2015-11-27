#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.3"
__author__ = "Zhongwei Sun (zhongwei.sun2008@gmail.com)"

# ----------------------------------------
# Example for using log.py
# ----------------------------------------

# build-in, 3rd party and my modules
import time
from ytlog import get_logger

log = get_logger({"name": "app", "dir": "./"})


if '__main__' == __name__:
    log.info("Mission starts.")
    wait_time = 2

    while True:
        log.info("Wait %s seconds" % wait_time)
        log.debug("I'm debug.")
        log.warning("I'm warning.")
        log.error("I'm error.")
        time.sleep(wait_time)
