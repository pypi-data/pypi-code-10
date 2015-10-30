"""
PTPathProfiler is a small page template expression profiler that monkey
expression classes to measure the speed of individual expressions

Copyright (c) 2003-2007 Infrae. All rights reserved.
See also LICENSE.txt
Version of this file: $Revision: 1.4 $
Written by Guido Wesdorp and other contributors
E-mail: guido@infrae.com
"""

# import the profiling machinery and monkeypatch the objects
from ProfilerPatch import PTProfilerPatch
from ProfilerPatch import ExprProfilerPatch
from ProfilerPatch import log

from zope.pagetemplate.pagetemplate import PageTemplate
from zope.tales.pythonexpr import PythonExpr
from zope.tales.expressions import PathExpr
from zope.tales.expressions import StringExpr

import PTProfilerViewer

def initialize(context):
    context.registerClass(
        PTProfilerViewer.PTProfilerViewer,
        constructors=(PTProfilerViewer.manage_addPTProfilerViewerForm,
                      PTProfilerViewer.manage_addPTProfilerViewer),
        icon='www/PTP.gif',
        )

    log('Patching page templates...')
    PTProfilerPatch(PageTemplate)
    log('Patching Z3 TALES engine...')
    ExprProfilerPatch('python', PythonExpr)
    ExprProfilerPatch('path', PathExpr)
    ExprProfilerPatch('string', StringExpr)
    log('Patched')
