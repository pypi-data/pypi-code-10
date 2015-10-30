import unittest

from Products.PTProfiler import testing
from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate


class TestInstall(unittest.TestCase):
    layer = testing.PTPROFILER

    def test_patched(self):
        from zope.pagetemplate.pagetemplate import PageTemplate
        self.assertTrue(hasattr(PageTemplate, '_patching_class'))


class TestViewer(unittest.TestCase):
    layer = testing.PTPROFILER_INTEGRATION

    def setUp(self):
        app = self.layer['app']

        from Products.PTProfiler.PTProfilerViewer import (
            manage_addPTProfilerViewer
        )
        manage_addPTProfilerViewer(app, 'ptviewer')
        self.ptviewer = app['ptviewer']

    def tearDown(self):
        self.ptviewer.disable()

    def test_enabled(self):
        self.assertFalse(self.ptviewer.enabled())
        self.ptviewer.enable()
        self.assertTrue(self.ptviewer.enabled())
        self.ptviewer.disable()
        self.assertFalse(self.ptviewer.enabled())

    def test_profiled(self):
        app = self.layer['app']
        manage_addPageTemplate(app, 'pttemplate')
        pttemplate = app['pttemplate']
        pttemplate.pt_edit('<p tal:content="string:test" />', 'text/html')
        self.assertTrue('test' in pttemplate())
        self.assertFalse(self.ptviewer.enabled())
        self.assertFalse(self.ptviewer.full_result())
        self.ptviewer.enable()
        pttemplate()
        self.assertTrue(self.ptviewer.full_result())
