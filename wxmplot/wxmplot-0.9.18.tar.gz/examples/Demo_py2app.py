from setuptools import setup
import epics
import sys
import os
import wx
import wx.lib.agw.flatnotebook
import numpy
import scipy
import matplotlib
matplotlib.use('WXAgg')

import sqlalchemy
import wxutils
import wxmplot
from wxmplot.plotframe import PlotFrame


APP = 'demo.py'


OPTIONS = {'includes': ['ConfigParser', 'Image', 'ctypes',
                        'fpformat',
                        'matplotlib', 'numpy', 'scipy',
                        'scipy.constants', 'scipy.fftpack',
                        'scipy.io.matlab.mio5_utils',
                        'scipy.io.matlab.streams', 'scipy.io.netcdf',
                        'scipy.optimize', 'scipy.signal',
                        'scipy.sparse.csgraph._validation', 'skimage',
                        'skimage.exposure', 'sqlalchemy',
                        'sqlalchemy.dialects.sqlite', 'sqlalchemy.orm',
                        'sqlalchemy.pool', 'sqlite3', 'wx', 'wx._core',
                        'wx.lib', 'wx.lib.*', 'wx.lib.agw',
                        'wx.lib.agw.flatnotebook',
                        'wx.lib.agw.pycollapsiblepane',
                        'wx.lib.colourselect', 'wx.lib.masked',
                        'wx.lib.mixins', 'wx.lib.mixins.inspection',
                        'wx.lib.newevent', 'wx.py', 'wxmplot', 'wxutils',
                        'wxversion', 'xml.etree',
                        'xml.etree.cElementTree'],
           'excludes': ['Tkinter', '_tkinter', 'Tkconstants', 'tcl',
                        'h5py.ipy_completer', 'IPython',
                        '_imagingtk', 'PIL._imagingtk', 'ImageTk',
                        'PIL.ImageTk', 'FixTk''_gtkagg', '_tkagg',
                        'matplotlib.tests',
                        'qt', 'PyQt4Gui', 'email', 'IPython'],
           'site_packages': True,
                        }
setup(app=[APP],  options={'py2app': OPTIONS})
