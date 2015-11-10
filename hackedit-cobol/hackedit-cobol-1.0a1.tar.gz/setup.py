#!/usr/bin/env python3
"""
Setup script for HackEdit
"""
import hackedit_cobol
from setuptools import setup, find_packages


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
    name='hackedit-cobol',
    version=hackedit_cobol.__version__,
    packages=[p for p in find_packages() if 'test' not in p],
    keywords=['IDE', 'Intergrated Development Environment', 'TextEditor',
              'Editor', 'COBOL', 'GnuCOBOL', 'OpenCOBOL', 'OpenCobolIDE'],
    url='https://github.com/HackEdit/hackedit-cobol',
    license='GPL',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description='A set of plugins that add COBOL support to HackEdit',
    long_description=long_desc,
    install_requires=['hackedit'],
    entry_points={
        # pyqode.cobol integration
        'hackedit.plugins.editors': [
            'CobolCodeEditPlugin = '
            'hackedit_cobol.plugins.editor:CobolCodeEditPlugin',
        ],
        # workspace plugins
        'hackedit.plugins.workspace_plugins': [
            'CobProjectManager = '
            'hackedit_cobol.plugins.project_mode:CobProjectManager',
            'CobFileManager = '
            'hackedit_cobol.plugins.file_mode:CobFileManager ',
            'CobOffsetCalculator = '
            'hackedit_cobol.plugins.offset:CobOffsetCalculator',
            'CobFileIndicators = '
            'hackedit_cobol.plugins.indicators:CobFileIndicators',
        ],
        # custom preference page plugin for the COBOL specific managers (
        # compilers, pre-parsers,...).
        'hackedit.plugins.preference_pages': [
            'CompilerPreferencesPlugin = hackedit_cobol.plugins.'
            'compiler_preferences:CompilerPreferencesPlugin',
            'PreparserPreferencesPlugin = hackedit_cobol.plugins.'
            'preparsers_preferences:PreparserPreferencesPlugin'
        ],
        # mimetype icon provider plugin
        'hackedit.plugins.file_icon_providers': [
            'CobolIconProvider = '
            'hackedit_cobol.plugins.icon_provider:CobolIconProvider'
        ],
        # plugin for indexing COBOL symbols
        'hackedit.plugins.symbol_indexors': [
            'CobSymbolIndexor = '
            'hackedit_cobol.plugins.indexor:CobolSymbolIndexor'
        ],
        # templates
        'hackedit.plugins.template_providers': [
            'CobTemplateProvider = '
            'hackedit_cobol.plugins.templates:CobTemplatesProvider'
        ],
        # workspaces
        'hackedit.plugins.workspace_providers': [
            'cobol_project_workspace = '
            'hackedit_cobol.plugins.workspaces:CobolProjectWorkspace',
            'cobol_file_workspace = '
            'hackedit_cobol.plugins.workspaces:CobolFileWorkspace'
        ]
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
