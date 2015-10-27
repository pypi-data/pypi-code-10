#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" Mix-in class for split widgets. """


# Enthought library imports.
from traits.api import Callable, Enum, Float, Interface


class ISplitWidget(Interface):
    """ Mix-in class for split widgets.

    A split widget is one that is split in two either horizontally or
    vertically.
    """

    #### 'ISplitWidget' interface #############################################

    #: The direction in which the widget is split.
    #
    #: Splitting vertically means there will be a left hand panel and a right
    #: hand panel, splitting horizontally means there will be a top panel and
    #: a bottom panel.
    direction = Enum('vertical', 'vertical', 'horizontal')

    #: The ratio of the size of the left/top pane to the right/bottom pane.
    ratio = Float(0.5)

    #: An optional callable that provides the left hand/top panel.
    lhs = Callable

    #: An optional callable that provides the right hand/bottom panel.
    rhs = Callable

    ###########################################################################
    # Protected 'ISplitWidget' interface.
    ###########################################################################

    def _create_splitter(self, parent):
        """ Create the toolkit-specific control that represents the widget.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control that contains the splitter.

        Returns
        -------
        splitter : toolkit control
            The toolkit control for the splitter.
        """

    def _create_lhs(self, parent):
        """ Creates the left hand/top panel depending on the direction.

        Parameters
        ----------
        parent : toolkit control
            The splitter's toolkit control.

        Returns
        -------
        lhs : toolkit control
            The toolkit control for the lhs.
        """

    def _create_rhs(self, parent):
        """ Creates the right hand/bottom panel depending on the direction.

        Parameters
        ----------
        parent : toolkit control
            The splitter's toolkit control.

        Returns
        -------
        rhs : toolkit control
            The toolkit control for the rhs.
        """


class MSplitWidget(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the ISplitWidget interface.
    """
