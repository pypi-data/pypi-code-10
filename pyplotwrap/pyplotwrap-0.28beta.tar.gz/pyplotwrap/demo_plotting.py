#==========================================================================
# Example to use plot wrapper function
#==========================================================================

import numpy
from copy import copy
from line_plots import plot_wrapper

#==========================================================================
# create data sets and store in dictionaries
#==========================================================================

t           = numpy.linspace(0,2*numpy.pi,100)

#==========================================================================
# First data set to be plotted
#==========================================================================

y1a         = numpy.sin(t)
y2a         = numpy.sin(2*t)
y3a         = numpy.sin(3*t)
y4a         = numpy.sin(4*t)

#==========================================================================
# Second data set to be plotted
#==========================================================================

y1b         = numpy.cos(t)
y2b         = numpy.cos(2*t)
y3b         = numpy.cos(3*t)
y4b         = numpy.cos(4*t)

#==========================================================================
# create level-2 dictionaries
#==========================================================================

#==========================================================================
# first waves
#==========================================================================

data1          = {}
data1['x']     = copy(t)
data1['xlbl']  = 'Time (seconds)'
data1['lstyle']= '-'          # line style
data1['mtype'] = 's'          # marker style
data1['set1']  = y1a          # data to be plotted on the y axis
data1['set2']  = y1b
data1['lcolor']= 'r'          # line color

#==========================================================================
# second set
#==========================================================================

data2          = {}
data2['x']     = copy(t)
data2['xlbl']  = 'Time (seconds)'
data2['lstyle']= '--'          # line style
data2['mtype'] = 'o'          # marker style
data2['set1']  = y2a          # data to be plotted on the y axis
data2['set2']  = y2b
data2['lcolor']= 'b'          # line color

#==========================================================================
# third set
#==========================================================================

data3          = {}
data3['x']     = copy(t)
data3['xlbl']  = 'Time (seconds)'
data3['lstyle']= '-'          # line style
data3['mtype'] = '^'          # marker style
data3['set1']  = y3a          # data to be plotted on the y axis
data3['set2']  = y3b
data3['lcolor']= 'k'          # line color

#==========================================================================
# fourth set
#==========================================================================

data4          = {}
data4['x']     = copy(t)
data4['xlbl']  = 'Time (seconds)'
data4['lstyle']= '--'          # line style
data4['mtype'] = '>'          # marker style
data4['set1']  = y4a          # data to be plotted on the y axis
data4['set2']  = y4b
data4['lcolor']= 'm'          # line color

#==========================================================================
# Level-2 dictionary data for keys in "keylist" will be plotted. The 
# y-axis label applied for each plot is the corresponding entry in ylabels
#==========================================================================

ylabels        = ['Sine Signal','Cosine Signal']
keylist        = ['set1','set2']

#==========================================================================
# Map level-2 dictionaries into level-1 dict for plotting
#==========================================================================

all_data       = {}
all_data['1']  = data1
all_data['2']  = data2
#all_data['3']  = data3
#all_data['4']  = data4
import os
path           = os.getcwd()
plot_wrapper(all_data, keylist, ylabels, path)
