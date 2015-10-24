#!/usr/bin/env python

import pycx4.pycda as cda

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


chan = cda.schan("localhost:1.name.6f")


cda.py_sl_main_loop()
