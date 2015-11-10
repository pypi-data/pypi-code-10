try:
    from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
except ImportError:
    RichIPythonWidget = None
    ipython_available = False
else:
    ipython_available = True


class PythonWorkspace:
    def get_data(self):
        data = {
          'name': 'Python',
          'description': 'Default pure python workspace.',
          'plugins': [
            'FindReplace',
            'DocumentOutline',
            'OpenDocuments',
            'Terminal',
            'PyRefactor',
            'PyRun',
            'PyContextMenus',
            'PyOpenModule',
            'PyCodeEditorIntegration',
            'CleanPycFiles'
            ]
        }
        if ipython_available:
            data['plugins'].append('IPythonConsole')
        return data
