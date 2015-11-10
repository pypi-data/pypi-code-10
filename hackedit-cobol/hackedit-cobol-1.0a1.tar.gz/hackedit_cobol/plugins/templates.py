"""
This module contains the COBOL templates provider plugin.
"""


class CobTemplatesProvider:
    def get_label(self):
        return 'COBOL'

    def get_remote_url(self):
        return 'https://github.com/HackEdit/cobol_templates.git'
