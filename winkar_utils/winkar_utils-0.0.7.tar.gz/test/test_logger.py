#!/usr/bin/env python

from utils import logger
import logging

import unittest
class factorTest(unittest.TestCase):
    def test_factor(self):
        try:
            print 
            logger.name = "test"
            logger.level = logging.DEBUG
            logger.info("test info")
            logger.debug("test debug")
            logger.warn("test warn")
            logger.error("test error")
        except Exception, e:
            print(e)
            raise AssertionError()
