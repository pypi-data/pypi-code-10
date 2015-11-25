# -*- coding: utf-8 -*-
u"""
This module implements the class that deals with the full document.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from builtins import super
from future import standard_library
standard_library.install_aliases()
import os
import subprocess
import errno
from .base_classes import Environment, Command
from .package import Package
from .utils import dumps_list, rm_temp_dir


class Document(Environment):
    ur"""
    A class that contains a full LaTeX document.

    If needed, you can append stuff to the preamble or the packages.
    For instance, if you need to use ``\maketitle`` you can add the title,
    author and date commands to the preamble to make it work.

    """

    def __init__(self, default_filepath=u'default_filepath', **_3to2kwargs):
        if 'data' in _3to2kwargs: data = _3to2kwargs['data']; del _3to2kwargs['data']
        else: data = None
        if 'lmodern' in _3to2kwargs: lmodern = _3to2kwargs['lmodern']; del _3to2kwargs['lmodern']
        else: lmodern = True
        if 'inputenc' in _3to2kwargs: inputenc = _3to2kwargs['inputenc']; del _3to2kwargs['inputenc']
        else: inputenc = u'utf8'
        if 'fontenc' in _3to2kwargs: fontenc = _3to2kwargs['fontenc']; del _3to2kwargs['fontenc']
        else: fontenc = u'T1'
        if 'documentclass' in _3to2kwargs: documentclass = _3to2kwargs['documentclass']; del _3to2kwargs['documentclass']
        else: documentclass = u'article'
        ur"""
        Args
        ----
        default_filepath: str
            The default path to save files.
        documentclass: str or `~.Command`
            The LaTeX class of the document.
        fontenc: str
            The option for the fontenc package.
        inputenc: str
            The option for the inputenc package.
        lmodern: bool
            Use the Latin Modern font. This is a font that contains more glyphs
            than the standard LaTeX font.
        data: list
            Initial content of the document.
        """

        self.default_filepath = default_filepath

        if isinstance(documentclass, Command):
            self.documentclass = documentclass
        else:
            self.documentclass = Command(u'documentclass',
                                         arguments=documentclass)

        fontenc = Package(u'fontenc', options=fontenc)
        inputenc = Package(u'inputenc', options=inputenc)
        # These variables are used for
        self._fontenc = fontenc
        self._inputenc = inputenc
        self._lmodern = inputenc
        if lmodern:
            lmodern = Package(u'lmodern')
        self.packages |= [fontenc, inputenc, lmodern]

        self.preamble = []

        super(Document, self).__init__(data=data)

    def dumps(self):
        u"""Represent the document as a string in LaTeX syntax.

        Returns
        -------
        str
        """

        head = self.documentclass.dumps() + u'\n'
        head += self.dumps_packages() + u'\n'
        head += dumps_list(self.preamble) + u'\n'

        return head + u'\n' + super(Document, self).dumps()

    def generate_tex(self, filepath=None):
        u"""Generate a .tex file for the document.

        Args
        ----
        filepath: str
            The name of the file (without .tex), if this is not supplied the
            default filepath attribute is used as the path.
        """

        super(Document, self).generate_tex(self._select_filepath(filepath))

    def generate_pdf(self, filepath=None, **_3to2kwargs):
        if 'silent' in _3to2kwargs: silent = _3to2kwargs['silent']; del _3to2kwargs['silent']
        else: silent = True
        if 'compiler_args' in _3to2kwargs: compiler_args = _3to2kwargs['compiler_args']; del _3to2kwargs['compiler_args']
        else: compiler_args = None
        if 'compiler' in _3to2kwargs: compiler = _3to2kwargs['compiler']; del _3to2kwargs['compiler']
        else: compiler = None
        if 'clean_tex' in _3to2kwargs: clean_tex = _3to2kwargs['clean_tex']; del _3to2kwargs['clean_tex']
        else: clean_tex = True
        if 'clean' in _3to2kwargs: clean = _3to2kwargs['clean']; del _3to2kwargs['clean']
        else: clean = True
        u"""Generate a pdf file from the document.

        Args
        ----
        filepath: str
            The name of the file (without .pdf), if it is `None` the
            ``default_filepath`` attribute will be used.
        clean: bool
            Whether non-pdf files created that are created during compilation
            should be removed.
        clean_tex: bool
            Also remove the generated tex file.
        compiler: `str` or `None`
            The name of the LaTeX compiler to use. If it is None, PyLaTeX will
            choose a fitting one on its own. Starting with mklatex and then
            pdflatex.
        compiler_args: `list` or `None`
            Extra arguments that should be passed to the LaTeX compiler. If
            this is None it defaults to an empty list.
        silent: bool
            Whether to hide compiler output
        """

        if compiler_args is None:
            compiler_args = []

        filepath = self._select_filepath(filepath)
        filepath = os.path.join(u'.', filepath)

        cur_dir = os.getcwdu()
        dest_dir = os.path.dirname(filepath)
        basename = os.path.basename(filepath)

        if basename == u'':
            basename = u'default_basename'

        os.chdir(dest_dir)

        self.generate_tex(basename)

        if compiler is not None:
            compilers = ((compiler, []),)
        else:
            latexmk_args = [u'--pdf']

            compilers = (
                (u'latexmk', latexmk_args),
                (u'pdflatex', [])
            )

        main_arguments = [u'--interaction=nonstopmode', basename + u'.tex']

        os_error = None

        for compiler, arguments in compilers:
            command = [compiler] + arguments + compiler_args + main_arguments

            try:
                output = subprocess.check_output(command,
                                                 stderr=subprocess.STDOUT)
            except (OSError, IOError), e:
                # Use FileNotFoundError when python 2 is dropped
                os_error = e

                if os_error.errno == errno.ENOENT:
                    # If compiler does not exist, try next in the list
                    continue
                raise(e)
            except subprocess.CalledProcessError, e:
                # For all other errors print the output and raise the error
                print(e.output.decode())
                raise(e)
            else:
                if not silent:
                    print(output.decode())

            if clean:
                try:
                    # Try latexmk cleaning first
                    subprocess.check_output([u'latexmk', u'-c', basename],
                                            stderr=subprocess.STDOUT)
                except (OSError, IOError), e:
                    # Otherwise just remove some file extensions.
                    extensions = [u'aux', u'log', u'out', u'fls',
                                  u'fdb_latexmk']

                    for ext in extensions:
                        try:
                            os.remove(basename + u'.' + ext)
                        except (OSError, IOError), e:
                            # Use FileNotFoundError when python 2 is dropped
                            if e.errno != errno.ENOENT:
                                raise

            if clean_tex:
                os.remove(basename + u'.tex')  # Remove generated tex file

            rm_temp_dir()

            # Compilation has finished, so no further compilers have to be
            # tried
            break

        else:
            # If none of the compilers worked, raise the last error
            raise(os_error)

        os.chdir(cur_dir)

    def _select_filepath(self, filepath):
        u"""Make a choice between ``filepath`` and ``self.default_filepath``.

        Args
        ----
        filepath: str
            the filepath to be compared with ``self.default_filepath``

        Returns
        -------
        str
            The selected filepath
        """

        if filepath is None:
            return self.default_filepath
        else:
            if os.path.basename(filepath) == u'':
                filepath = os.path.join(filepath, os.path.basename(
                    self.default_filepath))
            return filepath
