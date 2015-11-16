#!c:\Python35\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'WhatColorIsX==1.0.2','console_scripts','whatcoloris'
__requires__ = 'WhatColorIsX==1.0.2'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('WhatColorIsX==1.0.2', 'console_scripts', 'whatcoloris')()
    )
