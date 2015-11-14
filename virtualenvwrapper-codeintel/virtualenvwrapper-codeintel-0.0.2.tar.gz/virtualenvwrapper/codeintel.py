#!/usr/bin/env python
import sys
import os
import json
import logging


log = logging.getLogger(__name__)


def post_mkproject(args):
    """It reads current path and the
    project path, generating a CodeIntel configuration folder and file in JSON format
    """
    project_name = os.path.basename(os.getenv('VIRTUAL_ENV'))
    project_path = os.getenv('PROJECT_HOME')
    folder_name = '.codeintel'
    file_name = 'config'
    folder_path = os.path.join(project_path, project_name, folder_name)
    file_path = os.path.join(folder_path, file_name)
    python_bin = os.path.join('.', project_name, 'bin', 'python')
    python_version = sys.version_info[:2]
    python_version = str(python_version[0]) + '.' + str(python_version[1])
    extra_paths = os.path.join('.', project_name, 'lib', 'python' + python_version, 'site-packages')
    template = {
        "Python": {
            "python": python_bin,
            "pythonExtraPaths": [extra_paths]
        }
    }
    try:
        os.mkdir(folder_path)
    except OSError:
        pass
    with open(file_path, 'w') as target:
        target.write(json.dumps(template))
    return
