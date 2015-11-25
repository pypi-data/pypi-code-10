# -*- coding: utf-8 -*-
u"""
This module implements the class that deals with graphics.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from builtins import super
from future import standard_library
standard_library.install_aliases()
import os.path

from .utils import fix_filename, make_temp_dir, NoEscape, escape_latex
from .base_classes import UnsafeCommand, Float
from .package import Package
import uuid


class Figure(Float):
    u"""A class that represents a Figure environment."""

    packages = [Package(u'graphicx')]

    def add_image(self, filename, **_3to2kwargs):
        if 'placement' in _3to2kwargs: placement = _3to2kwargs['placement']; del _3to2kwargs['placement']
        else: placement = NoEscape(ur'\centering')
        if 'width' in _3to2kwargs: width = _3to2kwargs['width']; del _3to2kwargs['width']
        else: width = NoEscape(ur'0.8\textwidth')
        u"""Add an image to the figure.

        Args
        ----
        filename: str
            Filename of the image.
        width: str
            Width of the image in LaTeX terms.
        placement: str
            Placement of the figure, `None` is also accepted.

        """

        if placement is not None:
            self.append(placement)

        if width is not None:
            if self.escape:
                width = escape_latex(width)

            width = u'width=' + unicode(width)

        self.append(UnsafeCommand(u'includegraphics', options=width,
                                  arguments=fix_filename(filename)))

    def _save_plot(self, *args, **kwargs):
        u"""Save the plot.

        Returns
        -------
        str
            The basename with which the plot has been saved.
        """

        import matplotlib.pyplot as plt

        tmp_path = make_temp_dir()

        filename = os.path.join(tmp_path, unicode(uuid.uuid4()) + u'.pdf')

        plt.savefig(filename, *args, **kwargs)

        return filename

    def add_plot(self, *args, **kwargs):
        u"""Add the current Matplotlib plot to the figure.

        The plot that gets added is the one that would normally be shown when
        using ``plt.show()``.

        Args
        ----
        args:
            Arguments passed to plt.savefig for displaying the plot.
        kwargs:
            Keyword arguments passed to plt.savefig for displaying the plot. In
            case these contain ``width`` or ``placement``, they will be used
            for the same purpose as in the add_image command. Namely the width
            and placement of the generated plot in the LaTeX document.
        """

        add_image_kwargs = {}

        for key in (u'width', u'placement'):
            if key in kwargs:
                add_image_kwargs[key] = kwargs.pop(key)

        filename = self._save_plot(*args, **kwargs)

        self.add_image(filename, **add_image_kwargs)


class SubFigure(Figure):
    u"""A class that represents a subfigure from the subcaption package."""

    packages = [Package(u'subcaption')]

    #: By default a subfigure is not on its own paragraph since that looks
    #: weird inside another figure.
    separate_paragraph = False

    _repr_attributes_mapping = {
        u'width': u'arguments',
    }

    def __init__(self, width=NoEscape(ur'0.45\linewidth'), **kwargs):
        u"""
        Args
        ----
        width: str
            Width of the subfigure itself. It needs a width because it is
            inside another figure.

        """

        super(SubFigure, self).__init__(arguments=width, **kwargs)

    def add_image(self, filename, **_3to2kwargs):
        if 'placement' in _3to2kwargs: placement = _3to2kwargs['placement']; del _3to2kwargs['placement']
        else: placement = None
        if 'width' in _3to2kwargs: width = _3to2kwargs['width']; del _3to2kwargs['width']
        else: width = NoEscape(ur'\linewidth')
        u"""Add an image to the subfigure.

        Args
        ----
        filename: str
            Filename of the image.
        width: str
            Width of the image in LaTeX terms.
        placement: str
            Placement of the figure, `None` is also accepted.
        """

        super(SubFigure, self).add_image(filename, width=width, placement=placement)
