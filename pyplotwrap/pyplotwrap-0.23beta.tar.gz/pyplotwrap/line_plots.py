#=======================================================================
# Function to make line plot
#=======================================================================
from   pylab         import *
from   matplotlib    import pyplot
from   format_number import *  
#from   plot_fn       import save_png
import numpy
import os
import sys
import math

#=========================================================================
# function to plot multiple data sets stored in dictionaries and save pngs
#=========================================================================
   
def plot_wrapper(plot_data, keys, labels, save_folder):

   marker_size    = 7
   
#=========================================================================
# loop over all plots to create
#=========================================================================

   ikey           = 0
   print 'printing keys'
   for key,data in plot_data.iteritems():
      print 'data set name is ',key
      for k2,d2 in data.iteritems():
         print 'data subset name is ',k2

   for key,ylabel in zip(keys,labels):
      ikey        = ikey + 1
      print 'looking for ylabel id ',ylabel

#=========================================================================
# loop over all data sets
#=========================================================================
      
      plot_erase   = True
      for setname,dataset in plot_data.iteritems():


#=========================================================================
# extract x axis and plot options
#=========================================================================

         x     = dataset['x']
         xlbl  = dataset['xlbl']
         lsty  = dataset['lstyle']
         lcol  = dataset['lcolor']
         mtyp  = dataset['mtype']

#=========================================================================
# if key exists in dataset, plot it
#=========================================================================
   
         if key in dataset:
            print 'adding line for ',key
            y           = dataset[key]  
            fid         = ikey      
            a, ax,f     = draw_line_plot(x, y, ikey, lcol, mtyp, lsty,
                  2.2, marker_size, xlbl, ylabel, plot_erase)
            plot_erase  = False      # stop erasing figure when adding lines

#=======================================================================
# Outside the lines loop for a figure: change axes limits to have a
# small white box on bottom left corner
#=======================================================================

      # xticks            = a.get_xticks()
      # yticks            = a.get_yticks()

      # xticks            = a.get_xticks()
      # yticks            = a.get_yticks()
      # xtick2            = []
      # ytick2            = []
      # for tick in xticks:
      #    xtick2.append(format_number_AS(tick))
      # for tick in yticks:
      #    ytick2.append(format_number_AS(tick))

      # xmin  = xticks[0]    ;     xmax  = xticks[-1];  dx = xmax - xmin
      # ymin  = yticks[0]    ;     ymax  = yticks[-1];  dy = ymax - ymin#

#      xmin2 = xmin - 0.05*dx  ; xmax2 = xmax + 0.01*dx
#      ymin2 = ymin - 0.05*dy  ; ymax2 = ymax + 0.01*dy

#=======================================================================
# Draw a white line to blank out bottom axes in corner box
#=======================================================================

#      xt1   = [xmin2,xmin2+0.05*dx] ; yt1 = [ymin2, ymin2]
#      xt2   = [xmin2,xmin2]         ; yt2 = [ymin2, ymin2 + 0.05*dy]

#      print xmin2, xmax2, ymin2, ymax2

#      ax.plot(xt1,yt1,linewidth=1,color ='w', linestyle = '-')
#      ax.plot(xt2,yt2,linewidth=1,color ='w', linestyle = '-')

#      plt.set_xbound([xmin2,xmax2])  
#      plt.axis([xmin2,xmax2,ymin2,ymax2])

#      ax.set_xmargin(0.05)
#      plt.xticks(xtick2)
#      plt.xticks(ytick2)

#=======================================================================
# save the figure and close it
#=======================================================================

      img_name      = save_folder + os.sep + key
      save_png(img_name)
      print 'saving figure ',img_name
      plt.close(fid)
      
   return None

#=========================================================================
# function to plot multiple data sets 
#=========================================================================

def draw_line_plot(x, y,  fid, line_color, marker_type, line_style,      \
                   line_width,  marker_size, xlbl, ylbl, clear_fig):

#=======================================================================
# Set default font sizes for plotting
#=======================================================================

   plt.rc('text', usetex=True)

   font = {'family' : 'Times',
           'weight' : 'bold',
           'size'   : 20}

   matplotlib.rc('font', **font)

#=======================================================================
# determine marker interval
#=======================================================================
   
   mark_int = math.ceil(float(len(x))/16.0)

#=======================================================================
# draw a figure
#=======================================================================

   fig         = figure(fid)      

   if clear_fig:
      clf()

   ax          = fig.add_subplot(111)
   pyplot.plot(x,y,linewidth=line_width,color = line_color, linestyle = line_style,
                                marker = marker_type, markersize = marker_size,
                                markeredgewidth = 1.0,markeredgecolor = line_color,
                                markevery = mark_int)

#=======================================================================
#if plotting azimuth for rotorcraft, use [0,360] xticks
#=======================================================================

   if(xlbl[0:7].lower() == 'azimuth'):
      if(min(x) >= 0.0 and max(x) <= 360.0):
         pyplot.xlim(0.0,360.0)   
         xticks = numpy.arange(0,450,90)
         plt.xticks(xticks)

#=======================================================================
# create x and y labels, set ylabel rotation to 0
#=======================================================================

   if(xlbl != ''):
      plt.xlabel(xlbl,fontsize=18, fontweight='bold')
   if(ylbl != ''):
      plt.ylabel(ylbl,fontsize=18, fontweight='bold', rotation=0)
   
#=======================================================================
# move the labels to non-intrusive locations on plot
#=======================================================================

   ax.xaxis.set_label_coords(0.85 ,-0.07)
   ax.yaxis.set_label_coords(0.10,1.05)

#   ax.set_xmargin(0.01)
#=======================================================================
# make x,y grid values bold     
#=======================================================================

   a           = gca()
   xticks      = a.get_xticks()
   yticks      = a.get_yticks()
   xtick2      = []
   ytick2      = []
   for tick in xticks:
      xtick2.append(format_number_AS(tick))
   for tick in yticks:
      ytick2.append(format_number_AS(tick))
   a.set_xticklabels(xtick2, font)
   a.set_yticklabels(ytick2, font)

#=======================================================================
# turn on the grid      
#=======================================================================

   grid(True)

#=======================================================================
# Remove the "bounding box" lines to the top and right:
#=======================================================================

   for side in ['right','top']:
      ax.spines[side].set_visible(False)

#=======================================================================
# end of operations: return axes handle for additional postprocessing
#=======================================================================

   return a,ax,font

def save_png(filename):
      plt.savefig(filename+'.png',format='png',dpi=300)
