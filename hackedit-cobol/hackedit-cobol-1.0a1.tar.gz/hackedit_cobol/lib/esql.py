"""
Contains the code specific to esqlOC preparser integration.
"""
import os
from PyQt5 import QtWidgets


ESQL_CONFIG = {
    'name': 'SQL COBOL (esql)',
    'associated-extensions': ['*.sqb'],
    'path': '',  # to be filled
    'flags': '-static -o $file.cob $file.sqb',
    'output-rule': '$file.cob',
    'only-preparser': False,
    'extra-cobol-compiler-flags': '-l"%s\ocsql.lib"'
}


NAME = 'SQL COBOL (esql)'


def get_esql_config(parent):
    path, _ = QtWidgets.QFileDialog.getOpenFileName(
        parent, 'Select esql executable', filter='Executable (*.exe)')
    if path:
        cfg = ESQL_CONFIG.copy()
        cfg['path'] = os.path.normpath(path)
        cfg['extra-cobol-compiler-flags'] %= os.path.dirname(path)
        return cfg

    return None
