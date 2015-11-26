#!/usr/bin/env python

import unittest
import rhbz
import extension
from markdown import Markdown


class BugzillaExtensionTestCase(unittest.TestCase):

    # list of tuples (description, markup, expected)
    test_cases = [
(
"basic syntax",
"[bz#123]",
'<p><a href="http://bugzilla.example.com/123">bz#123</a></p>'
),
(
"upper case syntax",
"[BZ#123]",
'<p><a href="http://bugzilla.example.com/123">BZ#123</a></p>'
),
(
"string for bug number",
"[bz#error]",
'<p>[bz#error]</p>'
),
(
"dot for bug number",
"[bz#12.3]",
'<p>[bz#12.3]</p>'
),

]

    def setUp(self):
        self.md = Markdown(
                            extensions=['extension'],
                            extension_configs={
                                'extension' : {
                                    'bugzillaURL' : 'http://bugzilla.example.com/%s',
                                },
                            },
                        )

    def test_patterns_matching(self):
        for (description, markup, expected) in self.test_cases:
            self.assertEquals(self.md.convert(markup), expected.strip(), msg=description)

    def test_default_config(self):
        _ext = extension.makeExtension()
        self.assertEquals(_ext.config["bugzillaURL"][0], "%s")

    def test_broken_config(self):
        for url in ["invalid_format_string", "url_%s_with_2_%s"]:
            with self.assertRaises(extension.BugzillaExtensionException):
                _ext = extension.makeExtension(bugzillaURL=url)


class RedHatBugzillaExtensionTest(BugzillaExtensionTestCase):

    # list of tuples (description, markup, expected)
    test_cases = [
(
"rhbz basic syntax",
"[rhbz#123456]",
'<p><a href="https://bugzilla.redhat.com/show_bug.cgi?id=123456">rhbz#123456</a></p>'
),
(
"rhbz upper case syntax",
"[RHBZ#123]",
'<p><a href="https://bugzilla.redhat.com/show_bug.cgi?id=123">RHBZ#123</a></p>'
),

]

    def setUp(self):
        self.md = Markdown(extensions=['rhbz'])

    def test_default_config_is_redhat(self):
        _ext = rhbz.makeExtension()
        self.assertEquals(_ext.config["bugzillaURL"][0], "https://bugzilla.redhat.com/show_bug.cgi?id=%s")

    def test_custom_config_is_ignored(self):
        _ext = rhbz.makeExtension(bugzillaURL="http://bugzilla.example.com/%s")
        self.assertEquals(_ext.config["bugzillaURL"][0], "https://bugzilla.redhat.com/show_bug.cgi?id=%s")

if __name__ == "__main__":
    unittest.main()
