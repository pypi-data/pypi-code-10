#!/usr/bin/env python

import logging

logger = logging.getLogger("WinKaR")

logger.setLevel(logging.WARN)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
