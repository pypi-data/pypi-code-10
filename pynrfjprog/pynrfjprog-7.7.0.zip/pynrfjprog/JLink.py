
from __future__ import division
from __future__ import print_function

from builtins import int

import os
import sys
import os.path
import fnmatch


if sys.platform.lower().startswith('win'):
    _DEFAULT_SEGGER_ROOT_PATH = r'C:\Program Files (x86)\SEGGER'
elif sys.platform.lower().startswith('linux'):
    _DEFAULT_SEGGER_ROOT_PATH = r'/opt/SEGGER/JLink'


def find_latest_dll():

    if sys.platform.lower().startswith('win'):
        dir_list = [os.path.join(_DEFAULT_SEGGER_ROOT_PATH, folder) for folder in os.listdir(_DEFAULT_SEGGER_ROOT_PATH) if os.path.isdir(os.path.join(_DEFAULT_SEGGER_ROOT_PATH, folder))]
        if len(dir_list) == 0:
            return None

        versioned_list_dir = [(dir, _find_jlink_version_info(dir)) for dir in dir_list]
        sorted_versioned_list_dir = sorted(versioned_list_dir, key = lambda x: x[1])

        return os.path.join(sorted_versioned_list_dir[-1][0], 'JLinkARM.dll')
    
    elif sys.platform.lower().startswith('linux'):
        for filename in os.listdir(_DEFAULT_SEGGER_ROOT_PATH):
            if fnmatch.fnmatch(filename, '*.so.*.*'):
                return os.path.join(_DEFAULT_SEGGER_ROOT_PATH, filename)



def _find_jlink_version_info(segger_dir):

    return segger_dir[segger_dir.index('V') + 1:]
