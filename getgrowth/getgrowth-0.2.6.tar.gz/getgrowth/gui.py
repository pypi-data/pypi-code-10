# -*- coding: utf-8 -*-
import gtk
import numpy as np
import os
import subprocess
import matplotlib
matplotlib.use('GTKAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

import copy
import time
import my #My helper functions for stuff

class GUI(object):

    """ The GUI."""
    
    #The controlling object
    _controller=None
    
    #Widgets which will be referred to in the callbacks
    _w={}
    
    #Figures to draw curves on
    _uFig=None
    _LFig=None
    _uCanvas=None
    _lCanvas=None
    
    #Default background colors
    _defaultGray=None
    _defaultWhite=None
    
    _addingToGroup=None #Used when adding wells to a group
    _fittingRegression=None #Used when fitting regression lines
    _currentRegressionIsGroup=None
    _currentRegressionIndex=None
    
    #This is the number of the item currently being used for fitting regression lines
    #If there are N groups and M individual wells 0 to N-1 refer to groups and N to N+(M-1)
    #refer to wells
    _currentRegressionNumber=None
    
    def __init__(self,controller):
                    
        """Construct the GUI from the Glade file."""
        
        self._controller=controller #This contains the controlling object
        builder=gtk.Builder()
        builder.add_from_file(os.path.join(os.path.dirname(__file__),'gui.glade'))
        
        #Load all widgets which will be referred to in the callbacks       
        self._w['window']=builder.get_object('window')
        self._w['uFig']=builder.get_object('uFig')
        self._w['lFig']=builder.get_object('lFig')
        self._w['wellListStore']=builder.get_object('wellListStore')
        self._w['treeStore']=builder.get_object('treeStore')
        self._w['treeView']=builder.get_object('treeView')
        self._w['wellTreeView']=builder.get_object('wellTreeView')
        self._w['newGroup']=builder.get_object('newGroup')
        self._w['addToGroup']=builder.get_object('addToGroup')
        self._w['fitRegression']=builder.get_object('fitRegression')
        self._w['prevRegression']=builder.get_object('prevRegression')
        self._w['nextRegression']=builder.get_object('nextRegression')
        self._w['xScale']=builder.get_object('xScale')
        self._w['regressionLabel']=builder.get_object('regressionLabel')
        
        builder.connect_signals(self)
        
        #For setting the range of the slider
        self._w['xScale'].set_range(0.1,1)
        self._w['xScale'].set_value(1)
        
        #Figures for plotting
        self._uFig=Figure(figsize=(5,4),dpi=100)
        self._lFig=Figure(figsize=(5,4),dpi=100)
        
        self._uCanvas=FigureCanvas(self._uFig)
        self._uCanvas.set_size_request(800,300)
        self._lCanvas=FigureCanvas(self._lFig)
        self._lCanvas.set_size_request(800,300)
        self._lCanvas.mpl_connect('button_press_event',self.on_lCanvas_clicked)
        
        self._w['uFig'].add_with_viewport(self._uCanvas)
        self._w['lFig'].add_with_viewport(self._lCanvas)
        
        #Populate the wellListStore
        self._defaultGray=gtk.gdk.color_parse('#C9C9C9')
        self._defaultWhite=gtk.gdk.color_parse('#FFFFFF')
        
        gray=self._defaultGray
        white=self._defaultWhite
        self._w['wellListStore'].append(["↓", "↓", "↓", "↓", "↓", "↓", "↓", "↓",white,white,white,white,white,white,white,white,"○"])
        self._w['wellListStore'].append(["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",gray,gray,gray,gray,gray,gray,gray,gray,"→"])
        self._w['wellListStore'].append(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",gray,gray,gray,gray,gray,gray,gray,gray,"→"])
        self._w['wellListStore'].append(["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",gray,gray,gray,gray,gray,gray,gray,gray,"→"])
        self._w['wellListStore'].append(["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",gray,gray,gray,gray,gray,gray,gray,gray,"→"])
        self._w['wellListStore'].append(["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",gray,gray,gray,gray,gray,gray,gray,gray,"→"])
        self._w['wellListStore'].append(["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8",gray,gray,gray,gray,gray,gray,gray,gray,"→"])
        
        self._fittingRegression=False
        self._currentRegressionIsGroup=False
        self._currentRegressionIndex=None
        
        #Disable interface until some file has been loaded
        self.changeEnabled(False)

    def show(self):
        """ Show the GUI and enter main loop."""

        self._w['window'].show_all()
        gtk.timeout_add(100,gtk.main_iteration_do,True)
        gtk.idle_add(gtk.main_iteration_do,True)
        gtk.main()
        
    def plotData(self,x=0,y=0,colors=None,dashed=None,intervals=None,regressionResults=None,target=0):
        """ Plot data on the upper or lower figures.
        
            x:          N array with the time points
            y:          NxM array where N is the sample points and M is the samples
            colors:     Mx4 array in RGBA format
            dashed:     boolean vector with True if a sample should be plotted with
                        dashed line
            intervals:  Mx2 array with the limits for the linear regression. np.nan
                        is used if no interval is set
            """
            
        #Note that this is ignored if no color is supplied. Should be changed at some point
        if dashed is None:
            dashed=np.zeros(y.shape[1],dtype=bool)
        if intervals is None:
            intervals=np.zeros((y.shape[1],2))
            intervals[:]=np.nan
            
        if regressionResults is None:
            regressionResults=[None]*y.shape[1]
        
        #If target is upper
        if target is 0:
            ax=self._uFig.add_subplot(111)
        else:
            ax=self._lFig.add_subplot(111)
        
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min(), y.max())
        
        #This is to be able to use a LineCollection. This was a later addition and the
        #arguments for the function could be changed to get around this
            
        #First plot all solid lines
        if np.any(~dashed):
            segs=np.zeros((sum(~dashed), len(x), 2), float)
            segs[:,:,0]=x
            segs[:,:,1]=y.T[~dashed,:]

            lineCollection=matplotlib.collections.LineCollection(segs,colors=colors[~dashed,:])
        
            ax.add_collection(lineCollection)
        
        #Then dashed lines
        if np.any(dashed):
            segs=np.zeros((sum(dashed), len(x), 2), float)
            segs[:,:,0]=x
            segs[:,:,1]=y.T[dashed,:]

            lineCollection=matplotlib.collections.LineCollection(segs,colors=colors[dashed,:],linestyles='dotted')
        
            ax.add_collection(lineCollection)
            
        #Then add interval lines and regression results. This could also have been done
        #by a LineCollection, but since this is rather fast I keep it in a loop for now
        for interval,regressionResult in zip(intervals,regressionResults):
            
            #Draw vertical lines to indicate the regression limits
            if np.isnan(interval[0])==False:
                #Get the value for the non-dashed line at this point. Note that this
                #assumes that there will always be at least one non-dashed line when drawing
                #these marks
                refY=np.interp(interval[0],x,y[:,np.where(~dashed)[0][0]])
                ax.plot([interval[0],interval[0]],[refY-0.05*y.max(),refY+0.05*y.max()],linewidth=1,color=[0,0,0])
            if np.isnan(interval[1])==False:
                refY=np.interp(interval[1],x,y[:,np.where(~dashed)[0][0]])
                ax.plot([interval[1],interval[1]],[refY-0.05*y.max(),refY+0.05*y.max()],linewidth=1,color=[0,0,0])
            
            #Draw the regression information
            if not regressionResult is None:
                if target==0:
                    #Left part
                    rx=np.linspace(0,interval[0])
                    
                    if not np.isnan(regressionResult['ransac_intercept']):
                        ry=np.exp(regressionResult['ransac_intercept'])*np.power(np.exp(regressionResult['ransac_slope']),rx)
                        ax.plot(rx,ry,linewidth=1,color=[0.5,0.5,0.5],linestyle='-.')
                    ry=np.exp(regressionResult['intercept'])*np.power(np.exp(regressionResult['slope']),rx)
                    ax.plot(rx,ry,linewidth=1,color=[0,0,0],linestyle='-.')
                    
                    #Middle part
                    rx=np.linspace(interval[0],interval[1])
                    
                    if not regressionResult['ransac_intercept'] is None:
                        ry=np.exp(regressionResult['ransac_intercept'])*np.power(np.exp(regressionResult['ransac_slope']),rx)
                        ax.plot(rx,ry,linewidth=1,color=[0.5,0.5,0.5])
                    ry=np.exp(regressionResult['intercept'])*np.power(np.exp(regressionResult['slope']),rx)
                    ax.plot(rx,ry,linewidth=1,color=[0,0,0])
                    
                    #Right part
                    rx=np.linspace(interval[1],x.max())
                    
                    if not np.isnan(regressionResult['ransac_intercept']):
                        ry=np.exp(regressionResult['ransac_intercept'])*np.power(np.exp(regressionResult['ransac_slope']),rx)
                        ax.plot(rx,ry,linewidth=1,color=[0.5,0.5,0.5],linestyle='-.')
                    ry=np.exp(regressionResult['intercept'])*np.power(np.exp(regressionResult['slope']),rx)
                    ax.plot(rx,ry,linewidth=1,color=[0,0,0],linestyle='-.')
                    
                    if not regressionResult['upperLegend'] is None:
                        ax.text(0.02,0.9,regressionResult['upperLegend'] + ' (Normal)',fontsize=10,color=[0,0,0],transform = ax.transAxes)
                    if not regressionResult['ransac_upperLegend'] is None:
                        ax.text(0.02,0.82,regressionResult['ransac_upperLegend'] + ' (RANSAC)',fontsize=10,color=[0.5,0.5,0.5],transform = ax.transAxes)
                else:
                    #Left part
                    if not np.isnan(regressionResult['ransac_intercept']):
                        ry=[regressionResult['ransac_intercept'], regressionResult['ransac_intercept']+interval[0]*regressionResult['ransac_slope']]
                        ax.plot([0,interval[0]],ry,linewidth=1,color=[0.5,0.5,0.5],linestyle='-.')
                    ry=[regressionResult['intercept'], regressionResult['intercept']+interval[0]*regressionResult['slope']]
                    ax.plot([0,interval[0]],ry,linewidth=1,color=[0,0,0],linestyle='-.')
                        
                    #Middle part
                    if not np.isnan(regressionResult['ransac_intercept']):
                        ry=[regressionResult['ransac_intercept']+interval[0]*regressionResult['ransac_slope'], regressionResult['ransac_intercept']+interval[1]*regressionResult['ransac_slope']]
                        ax.plot(interval,ry,linewidth=1,color=[0.5,0.5,0.5])
                    ry=[regressionResult['intercept']+interval[0]*regressionResult['slope'], regressionResult['intercept']+interval[1]*regressionResult['slope']]
                    ax.plot(interval,ry,linewidth=1,color=[0,0,0])
                    
                    #Right part
                    if not np.isnan(regressionResult['ransac_intercept']):
                        ry=[regressionResult['ransac_intercept']+interval[1]*regressionResult['ransac_slope'], regressionResult['ransac_intercept']+x.max()*regressionResult['ransac_slope']]
                        ax.plot([interval[1],x.max()],ry,linewidth=1,color=[0.5,0.5,0.5],linestyle='-.')
                    ry=[regressionResult['intercept']+interval[1]*regressionResult['slope'], regressionResult['intercept']+x.max()*regressionResult['slope']]
                    ax.plot([interval[1],x.max()],ry,linewidth=1,color=[0,0,0],linestyle='-.')
                    
                    if not regressionResult['lowerLegend'] is None:
                        ax.text(0.02,0.9,regressionResult['lowerLegend'] + ' (Normal)',fontsize=10,transform = ax.transAxes)
                    if not regressionResult['ransac_lowerLegend'] is None:
                        ax.text(0.02,0.82,regressionResult['ransac_lowerLegend'] + ' (RANSAC)',fontsize=10,color=[0.5,0.5,0.5],transform = ax.transAxes)
        
        if target==0:
            ax.set_ylabel('original data')
        else:
            ax.set_ylabel('log-transformed data')
                                   
    def on_xScale_value_changed(self,widget,data=None):
        """ When the x-axis limit has been changed by the slider."""
        
        self._controller.setMaxTime(widget.get_value())
            
        #Re-scale x-axis. This check is because this is called once when the GUI is loaded, which is before the canvas exists
        if not self._uCanvas is None:
            if self._fittingRegression is False:
                #Clear figures
                self.clearFigures()
        
                #First plot all groups
                self.plotGroups(np.where(self._controller.toPlotGroups)[0])
                
                #Then add the individual wells
                self.plotWells(np.where(np.logical_and(self._controller.inGroup==False, self._controller.toPlot==True))[0])
                
                #Redraw figures
                self.redrawFigures()
            else:
                #If it's currently drawing a regression
                self.drawCurrentRegression()
            
    def on_menuSave_activate(self,widget,data=None):
        """ Export results to CSV file."""
        
        #Open save as dialog
        chooser=gtk.FileChooserDialog("Save File...", self._w['window'],
                                    gtk.FILE_CHOOSER_ACTION_SAVE,
                                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                    gtk.STOCK_SAVE, gtk.RESPONSE_OK))
                                    
        filter=gtk.FileFilter()
        filter.set_name("CSV files")
        filter.add_pattern("*.csv")
        chooser.add_filter(filter)
        
        chooser.set_current_name('GetGrowth results.csv')
    
        chooser.run()
        fileName=chooser.get_filename()
        chooser.destroy()
        
        if fileName is None:
            return
            
        #Append .csv if needed
        if not fileName[-4:].upper()=='.CSV':
            fileName=fileName+'.csv'
            
        self._controller.saveFile(fileName)
    
    def on_menuSample_activate(self,widget,data=None):
        """ Load a sample file."""
        
        self._controller.loadFile(os.path.join(os.path.dirname(__file__),'biolector.csv'))
            
        #Redraw the whole GUI (update color codes, plot all curves and so on)
        self.redrawGUI()
        self.changeEnabled(True,['prevRegression','nextRegression'])
        
                        
    def on_menuOpen_activate(self, widget, data=None):
        """ Select and open a Biolector file."""
        
        fileName=None
        
        chooser=gtk.FileChooserDialog("Open File...", self._w['window'],
                                      gtk.FILE_CHOOSER_ACTION_OPEN,
                                      (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                      gtk.STOCK_OPEN, gtk.RESPONSE_OK))
                                      
        filter=gtk.FileFilter()
        filter.set_name("CSV files")
        filter.add_pattern("*.csv")
        chooser.add_filter(filter)
                
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            fileName = chooser.get_filename()
            chooser.destroy()
        
        if not fileName is None:
            self._controller.loadFile(fileName)
            
            #Redraw the whole GUI (update color codes, plot all curves and so on)
            self.redrawGUI()
            self.changeEnabled(True,['prevRegression','nextRegression'])
            
    def plotGroups(self,groupIndexes,plotRegression=False):
        """ Plot groups on both upper and lower figure.
        
            The logarithm will be used for the values for the lower figure.
        """
        
        #Plot the data on the upper and lower figures
        values=None
        colors=None
        lines=None
        dashed=None
        intervals=None #Vertical lines to indicate regression interval
        regressions=None #Results structure from fitting
        
        if len(groupIndexes)>0:
            for index in groupIndexes:
                wells=self._controller.getGroupMembers(index)
                if len(wells)>0:
                    #Get which wells to plot and calculate the average values for them
                    I=self._controller.toPlot[wells]
                    wells=wells[I]
                    
                    if len(wells)>1:
                        meanValues=np.mean(self._controller.values[:,wells],1)[:,None]
                    else:
                        if len(wells)>0:
                            meanValues=self._controller.values[:,wells]
                        else:
                            #Nothing to display, continue
                            continue
                    
                    #Add to calculated means
                    gColor=self._controller.getGroupColor(index)[0]
                    if values is None:
                        values=meanValues
                        colors=gColor
                        dashed=np.zeros(1,dtype=bool)
                        if plotRegression is True:
                            intervals=self._controller.getGroupRegressionLimits(index)
                            regressions=self._controller.getGroupRegressionResults([index])
                        
                    else:
                        values=my.cat(values,meanValues,1)
                        colors=my.cat(colors,gColor,0)
                        dashed=my.cat(dashed,np.zeros(1,dtype=bool),0)
                        if plotRegression is True:
                            intervals=my.cat(intervals,self._controller.getGroupRegressionLimits(index),0)
                            regressions=regressions+self._controller.getGroupRegressionResults([index])
                        
                    #Also add the raw values for the members of the group
                    values=my.cat(values,self._controller.values[:,wells],1)
                    colors=my.cat(colors,np.tile(gColor,(len(wells),1)),0)
                    dashed=my.cat(dashed,np.ones(len(wells),dtype=bool),0)
                    
                    #There should not be drawn intervals for members of a group
                    if plotRegression is True:
                        nan=np.array([[np.nan,np.nan]])
                        intervals=my.cat(intervals,np.tile(nan,(len(wells),1)),0)
                        
                        #Or plotted regression lines
                        for i in range(0,len(wells)):
                            regressions.append(None)
            
            #It could be that no wells should be plotted
            if not values is None:
                if values.shape[1]>0:
                    #Plot data on upper figure
                    self.plotData(self._controller.timePoints,values,colors,dashed,intervals,regressions,0)
        
                    #Plot data on lower figure
                    self.plotData(self._controller.timePoints,np.log(values),colors,dashed,intervals,regressions,1)
                
    def plotWells(self,wellIndexes,plotRegression=False):
        """ Plot individual wells on both upper and lower figure.
        
            The logarithm will be used for the values for the lower figure.
        """
        intervals=None
        regressions=None
        
        if len(wellIndexes)>0:
            values=self._controller.values[:,wellIndexes]
            colors=self._controller.colors[wellIndexes,:]
            dashed=np.zeros(len(wellIndexes),dtype=bool)
            if plotRegression is True:
                intervals=self._controller.regressionLimits[wellIndexes,:]
                regressions=self._controller.getRegressionResults(wellIndexes)
            
            #Plot data on upper figure
            self.plotData(self._controller.timePoints,values,colors,dashed,intervals,regressions,0)
            
            #Plot data on lower figure
            self.plotData(self._controller.timePoints,np.log(values),colors,dashed,intervals,regressions,1)
            
    def redrawFigures(self):
        """ Redraw figures."""
        
        self._uCanvas.draw()
        self._lCanvas.draw()
        
    def clearFigures(self):
        """ Clear figures."""
        
        self._uFig.clear()
        self._lFig.clear()
            
    def redrawGUI(self):
        """ Redraw the whole GUI."""
        
        #Color the well labels
        self.colorWells()
        
        #Populate the TreeView with the wells
        self.updateTreeView()
        
        #Clear figures
        self.clearFigures()

        #First plot all groups
        self.plotGroups(np.where(self._controller.toPlotGroups)[0])
        
        #Then add the individual wells
        self.plotWells(np.where(np.logical_and(self._controller.inGroup==False, self._controller.toPlot==True))[0])
        
        #Redraw figures
        self.redrawFigures()
        
    def updateTreeView(self):
        """ Update the TreeView."""
        
        self._w['treeStore'].clear() #Clear everything
        #First add the groups
        if not self._controller.groupLabels is None:
            for i in range(0,len(self._controller.groupLabels)):
                #This is a little ugly, but I use negative indexes to represent groups and positive for wells
                #Note that it's "i-1" for groups to avoid 0 being an index for both wells and groups
                wells=self._controller.getGroupMembers(i)
                
                if self._controller.toPlotGroups[i]==False:
                    color=self._defaultGray
                else:
                    color=self._controller.getGroupColor(i)[1]
                    if color is None:
                        color=self._defaultWhite
                    
                group=self._w['treeStore'].append(None,[self._controller.groupLabels[i],color,self._controller.toPlotGroups[i],'   ',-i-1,True])
                
                #Then add the wells in the group
                for well in wells:
                    if self._controller.toPlot[well]==True:
                        wellcolor=color
                    else:
                        wellcolor=self._defaultGray
                    self._w['treeStore'].append(group,[self._controller.wellLabels[well],wellcolor,self._controller.toPlot[well],'   ',well,True])
                
        #Then add the individual wells
        for i in range(0,len(self._controller.wellLabels)):
            if self._controller.inGroup[i]==False:
                if self._controller.toPlot[i]==True:
                    color=gtk.gdk.Color(self._controller.colors[i,0],self._controller.colors[i,1],self._controller.colors[i,2])
                else:
                    color=self._defaultGray
                self._w['treeStore'].append(None,[self._controller.wellLabels[i],color,self._controller.toPlot[i],'   ',i,True])
    
    def colorWells(self):
        """ Set the colors for the well labels."""
        
        #Go through the groups and color all wells associated to them
        groups=self._controller.toPlotGroups
        if not groups is None:
            for i in range(0,len(groups)):
                wells=self._controller.getGroupMembers(i)
                if len(wells)>0:
                    #Use the color of the first well
                    color=self._controller.colors[wells[0],:]
                
                    for well in wells:
                        if self._controller.toPlot[well]==True:
                            self.setWellColor(well,color)
                        else:
                            self.setWellColor(well)
        
        #Then color wells which do not belong to a group
        I=np.where(self._controller.inGroup==False)
        
        for i in I[0]:
            if self._controller.toPlot[i]==True:
                self.setWellColor(i,self._controller.colors[i,:])
            else:
                self.setWellColor(i)
            
    def setWellColor(self,index,color=None):
        """ Set the color of an individual well.
        
        If color is not defined the default gray is used. Note that color is
        RBGA but that gdk.Color is used by the ListStore"""
        
        I=np.unravel_index(index,(6,8)) #Map from linear index
        
        if not color is None:
            self._w['wellListStore'][1+I[0]][I[1]+8]=gtk.gdk.Color(color[0],color[1],color[2])
        else:
            self._w['wellListStore'][1+I[0]][I[1]+8]=self._defaultGray

    def on_menuAbout_activate(self, widget, data=None):
        """ Display information about the software."""

        about = gtk.AboutDialog()
        about.set_program_name("GetGrowth")
        about.set_version("0.2")
        about.set_copyright("(c) Novo Nordisk A/S")
        about.set_comments("This software is not to be distributed outside of Novo Nordisk. Please contact Rasmus Ågren (RAAG) for any questions or comments.")
        about.run()
        about.destroy()
            
    def on_menuManual_activate(self, widget, data=None):
        """ Open the manual in the default PDF reader."""
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        subprocess.Popen(os.path.join(__location__, 'docs/manual.pdf'),shell=True)
        
    def on_window_destroy(self, widget, data=None):
        """ Quit the main GUI loop."""
        
        gtk.main_quit()
    
    def on_menuQuit_activate(self, widget, data=None):
        """ Close the window."""
        self._w['window'].destroy()
    
    #Callers
    def on_newGroup_clicked(self,widget,data=None):
        """ Catch clicks on the newGroup button."""
        
        #Only respond to the click if some data has been loaded
        if not self._controller.values is None:
            self._controller.newGroup()
            
            #Redraw the GUI. More specific functions should probably be used later
            self.redrawGUI()    
        
    def on_treeViewToggle_toggled(self,widget,data=None):
        """ Catch toggle for rows in the treeView."""
        
        #Get the index for the well/group
        I=self._w['treeStore'][data][4]
        
        #If it's a well
        if I>=0:
            self._controller.toggleToPlot(I)
        else:
            #If it's a group
            self._controller.toggleToPlotGroup(abs(I)-1)
        
        #Redraw the GUI. More specific functions should probably be used later
        self.redrawGUI()
    
    def on_treeViewLabels_edited(self,widget,data=None,newText=None):
        
        I=self._w['treeStore'][data][4]
        
        if I>=0:
            #If it's a well
            self._controller.setWellLabel(I,newText)
        else:
            #If it's a group
            self._controller.setGroupLabel(-1*I-1,newText)
            
        self.updateTreeView()
        
    def on_lCanvas_clicked(self,event):
        """ Catch clicks on the lower figure. This is used for setting intervals for
            the regression.
            
            Limits are set via left (for lower) and right (for upper) mouse clicks.
        """
        
        if self._fittingRegression==True:
            #The "not" in the if statements is to deal with the default value of np.nan()
            if self._currentRegressionIsGroup==True:
                if event.button==1:
                    #Don't do anything if it's higher than the upper limit
                    if not event.xdata>=self._controller._groupRegressionLimits[self._currentRegressionIndex,1]:
                        self._controller._groupRegressionLimits[self._currentRegressionIndex,0]=event.xdata
                #This should correspond to the right button. It's normally "3" but I'm not sure if that's always the case
                else:
                    if not event.xdata<=self._controller._groupRegressionLimits[self._currentRegressionIndex,0]:
                        self._controller._groupRegressionLimits[self._currentRegressionIndex,1]=event.xdata
                 
                #Perform the regression
                self._controller.fitGroup(self._currentRegressionIndex)       
                
            else:
                if event.button==1:
                    #Don't do anything if it's higher than the upper limit
                    if not event.xdata>=self._controller._regressionLimits[self._currentRegressionIndex,1]:
                        self._controller._regressionLimits[self._currentRegressionIndex,0]=event.xdata
                #This should correspond to the right button. It's normally "3" but I'm not sure if that's always the case
                else:
                    #Don't do anything if it's lower than the lower limit
                    if not event.xdata<=self._controller._regressionLimits[self._currentRegressionIndex,0]:
                        self._controller._regressionLimits[self._currentRegressionIndex,1]=event.xdata
                    
                #Perform the regression
                self._controller.fitLine(self._currentRegressionIndex)
             
            self.drawCurrentRegression()
            
    def changeEnabled(self,enable,exclude=['window']):
        """ Enable or disable all GUI components.

            enable:     true if the components should be enabled
            exclude:    list with names to exclude
        """
        
        if exclude is None:
            keys=self._w.keys
        else:
            keys=set(self._w.keys()) - set(exclude)
            
        #Exclude components which cannot be enabled/disabled or which belong to other windows
        keys=set(keys)-set(['wellListStore','treeStore'])
        for key in keys:
            self._w[key].set_sensitive(enable)
                 
    def drawCurrentRegression(self):
        """ Draw the current group/well being used for setting regression limits.
            Also update the regression label.
        """
        #Clear figures
        self.clearFigures()
        if self._currentRegressionIsGroup==True:
            self.plotGroups([self._currentRegressionIndex],True)
            toFit=self._controller._toPlotGroups
            self._w['regressionLabel'].set_label('Group ' + str(sum(toFit[:self._currentRegressionIndex+1])) + '/' + str(sum(toFit)) + ': ' + self._controller.groupLabels[self._currentRegressionIndex])
        else:
            self.plotWells([self._currentRegressionIndex],True)
            toFit=np.bitwise_and(self._controller._toPlot,~self._controller.inGroup)
            self._w['regressionLabel'].set_label('Well ' + str(sum(toFit[:self._currentRegressionIndex+1])) + '/' + str(sum(toFit)) + ': ' + self._controller.wellLabels[self._currentRegressionIndex])
            
        self.redrawFigures()
                
    def on_fitRegression_clicked(self,widget,data=None):
        """ Catch clicks on the fitRegression button."""
        
        if self._fittingRegression==False:
            self._fittingRegression=True
            self.shiftRegressionNumber()
            self.changeEnabled(False,['window','fitRegression','nextRegression','lCanvas','lFig','xScale','regressionLabel'])
            self._w['fitRegression'].set_label('Done')
            self._w['nextRegression'].set_sensitive(True) #It could be false since last fitting
        else:
            self._fittingRegression=False
            self.redrawGUI() #Redraw the whole GUI
            self._w['fitRegression'].set_label('Fit regression lines')
            self._w['regressionLabel'].set_label('')
            self.changeEnabled(True)
            self._w['prevRegression'].set_sensitive(False)
            self._w['nextRegression'].set_sensitive(False)
            
    def on_nextRegression_clicked(self,widget,data=None):
        """ Catch clicks on the nextRegression button."""
        
        #Should always be true
        if self._fittingRegression==True:
            self.shiftRegressionNumber(1)
    
    def on_prevRegression_clicked(self,widget,data=None):
        """ Catch clicks on the prevRegression button."""
        
        #Should always be true
        if self._fittingRegression==True:
            self.shiftRegressionNumber(-1)
    
    def shiftRegressionNumber(self,shift=0):
        """ Shift the regression item number and show the corresponding plots.
        
            shift: -1 for previous, 0 for reset to 0, 1 for next
        """
        
        if not self._controller.toPlotGroups is None:
            nGroups=sum(self._controller.toPlotGroups)
        else:
            nGroups=0
         
        if not self._controller.toPlot is None:
            nWells=sum(np.bitwise_and(self._controller.toPlot,~self._controller.inGroup))
        else:
            nWells=0
        
        #Reset to use the first element
        if shift==0:
            self._currentRegressionNumber=0
            
        if shift==-1:
            self._currentRegressionNumber=np.max((self._currentRegressionNumber-1,0))
        
        if shift==1:
            self._currentRegressionNumber=np.min((self._currentRegressionNumber+1,nGroups+nWells-1))
                    
        #Plot a group
        if nGroups>self._currentRegressionNumber:
            self._currentRegressionIsGroup=True
            gIds=np.where(self._controller.toPlotGroups)[0]
            self._currentRegressionIndex=gIds[self._currentRegressionNumber]
        else:
            self._currentRegressionIsGroup=False
            wIds=np.where(np.bitwise_and(self._controller.toPlot,~self._controller.inGroup))[0]
            self._currentRegressionIndex=wIds[self._currentRegressionNumber-nGroups]
                
        #Enable or disable the buttons
        self._w['prevRegression'].set_sensitive(True)
        self._w['nextRegression'].set_sensitive(True)
        if self._currentRegressionNumber==0:
            self._w['prevRegression'].set_sensitive(False)
        if self._currentRegressionNumber==nGroups+nWells-1:
            self._w['nextRegression'].set_sensitive(False)
        
        self.drawCurrentRegression() 
            
    def on_addToGroup_clicked(self,widget,data=None):
        """ Catch clicks on the addToGroup button."""
        
        if not self._controller.groupLabels is None:
            #Only do this if it's not already adding to a group
            if self._addingToGroup is None:
                #First check if there is a group selected in the treeView
                treeSelection = self._w['treeView'].get_selection()
                (model, pathlist)=treeSelection.get_selected_rows()
                
                #This should currently be only one, but for the future maybe
                for path in pathlist:
                    treeIter=model.get_iter(path)
                    value=model.get_value(treeIter,4)
                    
                    #Only do something if a group was selected
                    if value<0:
                        self._addingToGroup=abs(value)-1
                        self.changeEnabled(False,['window','wellTreeView','addToGroup'])
                        self._w['addToGroup'].set_label('Done')
            else:
                self._addingToGroup=None
                self.changeEnabled(True)
                self._w['addToGroup'].set_label('Add to selected group')           
    
    def on_wellTreeView_button_press_event(self,widget,data=None):
        """ Catch clicks on the wellTreeView.
        
            This is done in a rather inconvenient way since TreeViews are based
            around selecting cells and that leads to them being colored. To avoid
            that the indexes are calculated from the position of the click instead.
            
            This is very unstable and must be done better at some point.
        """
        
        #Only respond to the click if some data has been loaded
        if not self._controller.values is None:
            rect=widget.get_allocation()
            
            #Calculate indexes
            I=np.floor(9*data.x/rect.width)
            J=np.floor(7*data.y/rect.height)

            #If the click was on a well
            if I>0 and J>0:
                #Convert to linear index
                ind=np.int((J-1)*8+I-1)
                
                #Toggle whether to display the well or not or if it should be added to a group
                if self._addingToGroup is None:
                    self._controller.toggleToPlot(ind)
                else:
                    self._controller.addToGroup(self._addingToGroup,ind)
            else:
                #If the click was on a whole row/column
                if I==0 and J==0:
                    self._controller.toggleMultipleToPlot() #Toggle all
                else:
                    if I==0:
                        self._controller.toggleMultipleToPlot(J-1,0) #Toggle row
                    else:
                        self._controller.toggleMultipleToPlot(I-1,1) #Toggle column
            
            #Redraw the GUI. More specific functions should probably be used later
            self.redrawGUI()
        
        #I don't quite know how this works, but by returning True you inactivate the
        #selection of the row
        return True