"""
This module contains the COBOL templates provider plugin.
"""


class PyTemplatesProvider:
    def get_label(self):
        return 'Python'

    def get_remote_url(self):
        return 'https://github.com/HackEdit/python_templates.git'
