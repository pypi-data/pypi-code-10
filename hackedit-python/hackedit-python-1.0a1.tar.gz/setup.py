#!/usr/bin/env python3
"""
Setup script for hackedit-python
"""
from setuptools import setup, find_packages

import hackedit_python


# add build_ui command. This command is only used by developer to easily
# update the ui scripts.
# To use this command, you need to install the pyqt-distutils packages (using
# pip).
try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {'build_ui': build_ui}
except ImportError:
    build_ui = None
    cmdclass = {}

# get long description
with open('README.rst', 'r') as readme:
    long_desc = readme.read()


# run setup
setup(
    name='hackedit-python',
    version=hackedit_python.__version__,
    packages=find_packages(),
    keywords=['IDE', 'Intergrated Development Environment', 'TextEditor',
              'Editor'],
    url='https://github.com/HackEdit/hackedit-python',
    license='GPL',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='A set of plugins that add Python support to HackEdit',
    long_description=long_desc,
    data_files=[('share/hackedit_python', ['data/share/extlibs.zip'])],
    install_requires=['docutils'],
    entry_points={
        # our workspaces plugins (run script, ipython, rope,...)
        'hackedit.plugins.workspace_plugins': [
            'PyRun = hackedit_python.run:PyRun',
            'IPythonConsole = hackedit_python.ipython:IPythonConsole',
            'PyRefactor = hackedit_python.refactor:PyRefactor',
            'PyContextMenus = hackedit_python.context_menus:PyContextMenus',
            'PyOpenModule = hackedit_python.open_module:PyOpenModule',
            'PyCodeEditorIntegration = '
            'hackedit_python.editor:PyCodeEditorIntegration',
            'CleanPycFiles = hackedit_python.clean_pyc:CleanPycFiles'
        ],
        # custom preference page plugin for our python package manager
        'hackedit.plugins.preference_pages': [
            'interpreters = hackedit_python.interpreters:ManageInterpreters'
        ],
        'hackedit.plugins.symbol_indexors': [
            'PySymbolIndexor = hackedit_python.indexor:PySymbolIndexor'
        ],
        # builtin workspaces
        'hackedit.plugins.workspace_providers': [
            'python_workspace = hackedit_python.workspaces:PythonWorkspace'
        ],
        # templates
        'hackedit.plugins.template_providers': [
            'PyTemplatesProvider = '
            'hackedit_python.templates:PyTemplatesProvider'
        ],
        # pyqode.python editor integration
        'hackedit.plugins.editors': [
            'PyCodeEditorPlugin = hackedit_python.editor:PyCodeEditorPlugin',
        ],
    },
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)'
    ]
)
