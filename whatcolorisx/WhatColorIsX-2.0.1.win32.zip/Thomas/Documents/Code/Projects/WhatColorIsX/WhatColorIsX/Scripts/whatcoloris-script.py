#!c:\Users\Thomas\Documents\Code\Projects\WhatColorIsX\WhatColorIsX\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'WhatColorIsX==2.0.1','console_scripts','whatcoloris'
__requires__ = 'WhatColorIsX==2.0.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('WhatColorIsX==2.0.1', 'console_scripts', 'whatcoloris')()
    )
