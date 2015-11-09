#!/usr/bin/env python

# -* coding: utf-8 -*-

"""
python script to manage processes like:
1: app creation


Author: Tong Zhang
Created: Sep. 23rd, 2015
"""

import sys
import subprocess

if sys.argv[1] == "createApp":
    """
    do what createApp needs to do:
    """
    appname = sys.argv[2]

    # in folder: felapps
    # __init__.py
    
    # in folder: felapps/apps
    # create appname folder
    # in appname folder: touch __init__.py, appname.py

    # if create new util:
    # felapps/utils/newutils.py

    #
    # version number
    # felapps/utils/miscutils.py versionlist
    #
    
    # tests/test_felapps.py
