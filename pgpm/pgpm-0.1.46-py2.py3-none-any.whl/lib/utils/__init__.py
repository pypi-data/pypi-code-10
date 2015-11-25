import io
import logging
import os
import re

import pkg_resources

from pgpm import settings


def find_whole_word(w):
    """
    Scan through string looking for a location where this word produces a match,
    and return a corresponding MatchObject instance.
    Return None if no position in the string matches the pattern;
    note that this is different from finding a zero-length match at some point in the string.
    """
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def collect_scripts_from_sources(script_paths, files_deployment, is_package=False, logger=None):
    """
    Collects postgres scripts from source files
    :param script_paths: list of strings or a string with a relative path to the directory containing files with scripts
    :param files_deployment: list of files that need to be harvested. Scripts from there will only be taken
    if the path to the file is in script_paths
    :param is_package: are files packaged with pip egg
    :param logger: pass the logger object if needed
    :return:
    """
    logger = logger or logging.getLogger(__name__)
    scripts_dict = {}
    if script_paths:
        if not isinstance(script_paths, list):  # can be list of paths or a string, anyways converted to list
            script_paths = [script_paths]
        if is_package:
            for script_path in script_paths:
                for file_info in pkg_resources.resource_listdir('pgpm', script_path):
                    scripts_dict[file_info] = pkg_resources.resource_string('pgpm', '{0}/{1}'
                                                                            .format(script_path, file_info))\
                        .decode('utf-8')
                    logger.debug('{0}/{1}'.format(script_path, file_info))
        else:
            for script_path in script_paths:
                for subdir, dirs, files in os.walk(script_path):
                    files = sorted(files)
                    for file_info in files:
                        if file_info != settings.CONFIG_FILE_NAME:
                            if files_deployment:  # if specific script to be deployed, only find them
                                for list_file_name in files_deployment:
                                    if file_info == list_file_name:
                                        scripts_dict[list_file_name] = io.open(os.path.join(subdir, file_info),
                                                                               'r', -1, 'utf-8', 'ignore').read()
                                        logger.debug('{0}'.format(os.path.join(subdir, file_info)))
                            else:
                                scripts_dict[file_info] = io.open(os.path.join(subdir, file_info),
                                                                  'r', -1, 'utf-8', 'ignore').read()
                                logger.debug('{0}'.format(os.path.join(subdir, file_info)))
    return scripts_dict
