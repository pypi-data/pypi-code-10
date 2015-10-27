#!/usr/bin/env python

import glob
import os

def cleanup_directory():
    for filename in glob.glob( '__result*' ): 
        os.unlink(filename)

cleanup_directory()

