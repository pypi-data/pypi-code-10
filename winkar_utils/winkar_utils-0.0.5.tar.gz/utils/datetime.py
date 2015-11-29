#!/usr/bin/env python

import time

def now():
    # import pdb; pdb.set_trace()
    # TODO
    # create a class with __str__ return this
    return time.strftime('%Y-%m-%d %X', time.localtime())
