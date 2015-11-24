#!/usr/bin/env python


import os, sys

if sys.version_info >= (3, ):
    #Python3
    os.environ["PINGUINO_PYTHON"] = "3"
else:
    #Python2
    os.environ["PINGUINO_PYTHON"] = "2"

# Python3 compatibility
if os.getenv("PINGUINO_PYTHON") is "3":
    import imp
    imp.reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
