#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cobol backend server which adds a CobolCodeCompletionProvider and a
DocumentWordsProvider to the CodeCompletion worker.
"""
import sys
import os

sys.path.insert(0, os.environ['HACKEDIT_LIBS_PATH'])

from PyQt5.QtCore import QCoreApplication
from cement.core import exc
from pyqode.cobol.backend.workers import CobolCodeCompletionProvider
from pyqode.core import backend


if __name__ == '__main__':
    # setup QApplication so that we can use QSettings (we're in a background
    # process here!)
    QCoreApplication.setOrganizationName('HackEdit')
    QCoreApplication.setOrganizationDomain('hackedit.com')
    QCoreApplication.setApplicationName('HackEdit')

    backend.CodeCompletionWorker.providers.append(
        CobolCodeCompletionProvider())
    backend.DocumentWordsProvider.separators.remove('-')
    backend.CodeCompletionWorker.providers.append(
        backend.DocumentWordsProvider())
    try:
        backend.serve_forever()
    except exc.CaughtSignal as e:
        sys.exit(0)
