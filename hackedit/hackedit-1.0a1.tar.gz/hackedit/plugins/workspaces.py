"""
This module contains the core builtin workspaces...
"""


class EmptyWorkspace:
    def get_data(self):
        return {
            'name': 'Empty',
            'description': 'Empty workspace',
            'plugins': [
            ]
        }


class GenericWorkspace:
    def get_data(self):
        return {
            'name': 'Generic',
            'description': 'Generic default workspace',
            'plugins': [
                'FindReplace',
                'DocumentOutline',
                'OpenDocuments',
                'Terminal'
            ]
        }
