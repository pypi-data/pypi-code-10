#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
plotEnv
=======

Custom plotting environment using seaborn (based on Matplotlib). Color scheme using
flat ui (http://designmodo.github.io/Flat-UI/).


:First Added:   2015-05-25
:Last Modified: 2015-11-27
:Author:        Lento Manickathan

"""

# Import required modules
import numpy as _np
import matplotlib as _mpl
from matplotlib import pyplot as _plt
from seaborn import despine as _despine

# CONSTANTS
RED     = '#e74c3c'
YELLOW  = '#f1c40f'
GREEN   = '#2ecc71'
BLUE    = '#3498db'
VIOLET  = '#8e44ad'
DARK    = '#2c3e50'
GRAY    = '#7f8c8d'
DARKGREEN = '#16a085'
ORANGE  = '#d35400'

MARKERTYPES = ['o', 's', 'D', 'v', '^', '<', '>','*', ',', '.', 'p', 'd']

DEFAULT_RCPARAMS = {'axes.axisbelow'  : True,
                    'axes.edgecolor'  : '0.15',
                    'axes.facecolor'  : 'white',
                    'axes.labelcolor' : '0.15',
                    'axes.grid'       : False,
                    'axes.labelsize'  : 16,
                    'axes.linewidth'  : 1.25,
                    'axes.titlesize'  : 12,
                    'figure.figsize'  : _np.array([2./(_np.sqrt(5)-1), 1])*5,
                    'font.family'     : ['sans-serif'],
                    'font.sans-serif' : ['Arial', 'Liberation Sans',
                                         'Bitstream Vera Sans', 'sans-serif'],
                    'grid.color'      : '0.8',
                    'grid.linestyle'  : '-',
                    'grid.linewidth'  : 1,
                    'interactive'     : True,
                    'legend.fontsize' : 10,
                    'legend.frameon'  : False,
                    'legend.loc'      : 'best',
                    'legend.numpoints': 1,
                    'legend.scatterpoints' : 1,
                    'lines.linewidth' : 1.2,
                    'lines.markeredgewidth' : 0.,
                    'lines.markersize': 7,
                    'lines.solid_capstyle' : 'round',
                    'patch.linewidth' : .3,
                    'savefig.dpi'     : 250,
                    'savefig.format'  : 'pdf',
                    'text.color'      : '0.15',
                    'xtick.color'     : '0.15',
                    'xtick.direction' : 'out',
                    'xtick.labelsize' : 14,
                    'xtick.major.pad' : 7,
                    'xtick.major.size': 6,
                    'xtick.minor.size': 3,
                    'ytick.color'     : '0.15',
                    'ytick.direction' : 'out',
                    'ytick.labelsize' : 14,
                    'ytick.major.pad' : 7,
                    'ytick.major.size': 6,
                    'ytick.minor.size': 3}

def set(plotType='line', numColors=1, interactive=True):
    """

    Parameters
    ----------
    plotType : 'line', 'surface'

    numColors : int, or one of {1 (default), 3, 9}
                The number of colour required for plotting.

    interactive : bool
                  Turn plot interactive on

    See Also
    --------
    Palette : Line plot
                Flat ui: http://designmodo.github.io/Flat-UI/
              Surface plot
                matplotlib 'Spectral'

    Examples
    --------
    >>> palette = set(plotType='line', numColors=2)
    or
    >>> palette = set(plotType='surface')

    """

    # Set matplotlib rc parameters
    rcParams = DEFAULT_RCPARAMS

    # Set plot interactive on/off
    rcParams['interactive'] = interactive

    # Determine plot type
    if plotType == 'line':

        # Set Palette
        palette = linePlotPalette(numColors)
        rcParams['axes.color_cycle'] = list(palette)

    elif plotType == 'surface':

        # Set Palette
        palette = surfacePlotPalette()

    else:
        return NotImplementedError('plot type unknown or not implemented')

    # Set matplotlib rc parameters
    _mpl.rcParams.update(rcParams)

    return palette


def linePlotPalette(numColors):
    """
    Returns plot palette. Color palette : Flat ui: http://designmodo.github.io/Flat-UI/

    Parameters
    ----------
    numColors : int, or one of {1 (default), 3, 9}
                The number of colour required for plotting.

    Examples
    --------
    >>> palette = linePlotPalette(numColors=4)
    or

    """

    # Define the color palatte
    if numColors == 1:
        # Midnight blue
        palette = [DARK]
    elif numColors == 2:
        # Alizarin, Peter river
        palette = [RED, BLUE]
    elif numColors == 3:
        # Alizarin, Emerald, Peter river
        palette = [RED, GREEN, BLUE]
    elif numColors >= 4 and numColors <= 9:
        # Alizarin, Sun Flower, Emerald, Peter river, Wisteria, Midnight blue
        # Asbestos, Green sea, Pumpkin
        palette = [RED, YELLOW, GREEN, BLUE, VIOLET, DARK, GRAY, DARKGREEN, ORANGE][:numColors]
    else:
        return NotImplementedError('numColors should be 1 to 9.')

    return palette


def surfacePlotPalette():
    """
    Surface plot palette

    Divergent colormap [cold (blue)-> hot (red)]

    Sequential colormaps: 1) Cold, 2) Hot

    """

    return dict(DIV = _mpl.cm.Spectral_r,
                SEQ_HOT_R  = _mpl.colors.ListedColormap(_mpl.cm.Spectral(_np.arange(0,128))),
                SEQ_COLD   = _mpl.colors.ListedColormap(_mpl.cm.Spectral(_np.arange(128,256))),
                SEQ_HOT    = _mpl.colors.ListedColormap(_mpl.cm.Spectral_r(_np.arange(128,256))),
                SEQ_COLD_R  = _mpl.colors.ListedColormap(_mpl.cm.Spectral_r(_np.arange(0,128))))


def cleanupFigure(despine=True, tightenFigure=True,):
    """
    Cleans up the figure by:
        1) Removing unnecessary top and right spines using seaborn's `despine` function
        2) Tighten the figure using pyplot's `tight_layout` function

    Parameters
    ----------
    despine : bool, True (default) or False

    tightenFigure : bool, True (default) or False


    See Also
    --------
    seaborn.despine : Seaborn's despine function

    pyplot.tight_layout : Function to adjust the subplot padding


    Examples
    --------
    >>> cleanupFigure(despine=True, tightenFigure=True)

    """

    # Remove extra spline
    if despine:
        _despine()

    # Remove the extra white spaces
    if tightenFigure:
        _plt.gcf().tight_layout()

    # Re-draw plot
    _plt.draw()


def colorbar(ticks,orientation='vertical',splitTicks=False,**kw):
    """
    Customized colorbar
    """

    # determine colorbar position
    if orientation[0]=='h':
        orientation='horizontal'
        aspect=40
        if splitTicks:
            pad=0.25
        else:
            pad=0.2
    elif orientation[0]=='v':
        orientation='vertical'
        aspect=25
        pad=0.05
    else:
        ValueError("orientation '%s' unknown" % orientation)

    # Default colorbar params
    cbParams = {'aspect'       : aspect,
                'drawedges'    : True,
                'format'       : '%.2g',
                'orientation'  : orientation,
                'pad'          : pad,
                'spacing'      : 'proportional',
                'ticks'        : ticks}

    # Modify cb params
    cbParams.update(kw)

    if cbParams['format'] == 'exp':
        cbParams['format'] = None # Default

    # Draw colorbar
    cb = _plt.colorbar(**cbParams)

    # Split ticks
    if splitTicks:
        if orientation[0] == 'h':
            # Change ticks position
            if _np.any(ticks<0) and _np.any(ticks>0):
                for v,t in zip(ticks,cb.ax.xaxis.majorTicks):
                    if v>0:
                        t._apply_params(gridOn=False,label1On=False,label2On=True,
                                        tick1On=False,tick2On=True)
        elif orientation[0] == 'v':
            NotImplementedError("orientation 'vertical' not implemented")
        else:
            ValueError("orientation '%s' unknown" % orientation)

    # Redraw plot
    _plt.draw()

    return cb
