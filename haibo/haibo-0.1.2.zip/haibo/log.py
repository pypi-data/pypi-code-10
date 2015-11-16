#!/usr/bin/env python
# encoding: utf8

'''
Date:2014-04-10
Author:whb
'''

import logging
import sys

LOG_FORMAT = '%(asctime)s - %(levelname)s: %(message)s'
LEVEL = "INFO"

def loginfo(msg,fileName="/tmp/tmp.log"):
    try:
        print msg
        logging.basicConfig(filename = fileName,
                level = LEVEL,
                filemode='w',
                format = LOG_FORMAT)
    except:
        sys.stderr.write('mv log path to /tmp/tmp.log\n')
        logging.basicConfig(filename = '/tmp/tmp.log',
                level = LEVEL,
                filemode='w',
                format = LOG_FORMAT)
    finally:
        logging.info(msg)
        

if __name__ == '__main__':
    for i in range(1,5):
        print i
        loginfo(i,"/etc/test.log")
