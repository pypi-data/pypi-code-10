# -*- coding: utf-8 -*-

from gui import GUI
import csv
import numpy as np
import matplotlib #This is only for getting the default colors
import gtk
import my #Some helper functions
#import Tkinter #This should not be required, but is needed for Py-Installer
#import FileDialog #This should not be required, but is needed for Py-Installer
#import scipy.linalg.cython_blas #This should not be required, but is needed for Py-Installer
#import scipy.linalg.cython_lapack #This should not be required, but is needed for Py-Installer
#import scipy.special._ufuncs_cxx #This should not be required, but is needed for Py-Installer
import statsmodels as sm
import statsmodels.api as sma
import statsmodels.formula.api as smf
import pandas as pd #For the DataFrame object
import warnings
#import cProfile

class GetGrowth(object):
    """ Main controller for the GetGrowth software.
        
        Performs calculations and serves as an interface to the GUI
    """
    
    #The GUI. This will also display the GUI
    _gui=None
    _times=None #Vector with the measured times
    _maxTime=1 #This can be used for setting an upper limit on the times (and corresponding values) which are returned. 0-1
    _values=None #Nx48 array with the measured values
    _toPlot=None #Boolean vector which determines if a well should be plotted and participate in calculations
    _wellColors=None #Nx4 array with the RGBA color to use for each well
    _plateDim=None #Tuplet with the dimensions of the plate
    _wellLabels=None #The labels for individual well (not groups)
    _inGroup=None #Boolean vector with True if a well is a member of a group
    _regressionLimits=None #48x2 array with the limits for the linear regression. NaN is used when the values haven't been set
    _regressionResults=None #list with the interpolation results for an individual well. NaN is used when the values haven't been set
    _delimiter=None #The delimiter used when loading the latest CSV file. This is also used when exporting, in order to maintain copmatibility
    
    _groupCounter=None #Counter for how many groups have been created. Used in the naming of groups
    _groupLabels=None #The labels for groups
    _toPlotGroups=None #Boolean vector which determines if a group should be plotted and participate in calculations
    _groupMembers=None #List of lists with the wells for each group
    _groupRegressionLimits=None #Nx2 array with the limits for the linear regression. NaN is used when the values haven't been set
    _groupRegressionResults=None #list with the interpolation results for a group. NaN is used when the values haven't been set
    
    #Properties       
    @property
    def timePoints(self):
        """ Array of timepoints for the measurements."""
        if self._maxTime==1:
            return self._times
        else:
            #Crop to maxTime
            return self._times[self._times<=(self._maxTime*self._times[-1])]
    @property
    def wellLabels(self):
        """ List of labels for the individual wells."""
        
        return self._wellLabels
     
    @property
    def values(self):
        """ Array with measurements for the wells."""
        
        if not self._values is None:
            if np.isinf(self._maxTime):
                return self._values
            else:
                #Crop to maxTime
                return self._values[self._times<=(self._maxTime*self._times[-1]),:]
        else:
            return None

    @property
    def toPlot(self):
        """ Boolean array with the wells to plot."""
        
        return self._toPlot
    
    @property
    def colors(self):
        """ Array with colors for the individual wells."""
        
        return self._wellColors
        
    @property
    def regressionLimits(self):
        """ Nx2 array with regression limits for the individual wells."""
        
        return self._regressionLimits
         
    @property
    def groupLabels(self):
        """ Array with labels for the groups."""
        
        return self._groupLabels
        
    @property
    def toPlotGroups(self):
        """ Boolean array with the groups to plot."""
        
        return self._toPlotGroups
        
    @property
    def inGroup(self):
        """ Boolean array which determines if a well participates in a group."""
        
        return self._inGroup
        
    def __init__(self):
        self.initVariables()
        
    def showGUI(self):
        """ Load and show the GUI."""
        
        self._gui=GUI(self)
        
        #Show GUI and give control over to the main GUI loop
        self._gui.show()
        
    def setMaxTime(self,value):
        """ Set the maximal time factor."""
        self._maxTime=value
    
    def initVariables(self):
        """ (Re)set all variables to their default values """
        
        self._toPlot=np.ones(48,dtype=bool)
        self._inGroup=np.zeros(48,dtype=bool)
        self._regressionLimits=np.empty((48,2))
        self._regressionLimits[:]=np.nan
        self._regressionResults=[None]*48
        self._wellLabels=["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
                        "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8",
                        "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8",
                        "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
                        "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
                        "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]
        self._times=None
        self._values=None
        self._wellColors=matplotlib.cm.gist_rainbow(np.linspace(0,1,48))
        self._plateDim=(6,8)
        self._groupCounter=1
        self._groupLabels=None
        self._toPlotGroups=None
        self._groupMembers=None
        self._groupRegressionLimits=None
        self._groupRegressionResults=None
        
    def fitGroup(self,index):
        """ Fits a Random intercept, random slope-model to the curves in a group. Note
            that the log of the values will be used and that the fitting will be done in
            the interval specified by regressionLimits.
        """
        
        startT=self._groupRegressionLimits[index,0]
        endT=self._groupRegressionLimits[index,1]
        
        if not np.isnan(startT) and not np.isnan(endT):
            #Get the data. 
            I=np.where(np.bitwise_and(self._times>=startT, self._times<=endT))[0]
            
            p=np.log(self._values[I,:])
            
            members=self._groupMembers[index]
            
            data=np.zeros((0,3))
            
            
            for i in range(0,len(members)):
                toAdd=np.column_stack((self._times[I],p[:,members[i]],i*np.ones((len(I),1))))
                data=np.row_stack((data,toAdd))
                
                #Also fit a line to each member. This is not used here, but is printed when saving
                self._regressionLimits[members[i],0]=startT
                self._regressionLimits[members[i],1]=endT
                self.fitLine(members[i])
            
            result=self._MELR(data)
            ransacResult=self._fitRANSAC(data[:,0],data[:,1],data[:,2],[self._regressionResults[i] for i in members])
            
            if not ransacResult is None:
                result['ransac_intercept']=ransacResult['intercept']
                result['ransac_slope']=ransacResult['slope']
                result['ransac_confInterval']=ransacResult['confInterval']
                result['ransac_upperLegend']=ransacResult['upperLegend']
                result['ransac_lowerLegend']=ransacResult['lowerLegend']
            else:
                result['ransac_intercept']=np.nan
                result['ransac_slope']=np.nan
                result['ransac_rsquared']=np.nan
                result['ransac_confInterval']=[np.nan,np.nan]
                result['ransac_upperLegend']='No model found'
                result['ransac_lowerLegend']='No model found'
            self._groupRegressionResults[index]=result
        
    def _fitRANSAC(self,t,y,types=None,prevFit=None):
        """ Performs a robust linear regression using the RANSAC algorithm.
        
            types:      the line index for each value in y (if for a group)
            prevFit:    a result structure or a list of result structures (if for a group) 
        
            Returns a results dictionary
        """
        
        #RANSAC parameters
        proportionToInclude=0.7
        minProportionForModel=0.7
        nIterations=500
        
        #To be able to run same code for groups
        if types is None:
            singleFit=True
            types=np.zeros(len(t))
        else:
            singleFit=False
            
        if isinstance(prevFit,dict):
            prevFit=[prevFit]
        
        #True if a point is in the final fitting
        inPoints=np.zeros(len(t),dtype=bool)
        
        #Do this for each line
        for i in range(0,len(prevFit)):
            I=np.where(types==i)[0]
            
            #First get the points from the previous fit
            oldY=prevFit[i]['intercept']+t[I]*prevFit[i]['slope']
            
            #Ignore points which have larger residuals than this
            maxRes=np.percentile(np.sort(np.abs(oldY-y[I])),proportionToInclude*100)
            
            for j in range(0,nIterations):
                #Select two random points in the range
                limits=np.random.choice(len(I),2,replace=False)
                x0=min(limits)
                x1=max(limits)
                
                #Calculate the line between the two points
                slope=(y[I[x1]]-y[I[x0]])/(t[I[x1]]-t[I[x0]])
                intercept=y[I[x0]]-t[I[x0]]*slope
                
                #Calculate the predicted points for the line
                p=intercept+slope*t[I]
                
                goodFits=np.abs(p-y[I])<=maxRes
                if sum(goodFits)>=minProportionForModel*len(I):
                    inPoints[I]=np.bitwise_or(inPoints[I],goodFits)
        
        #Perform linear regression on all inPoints
        if any(inPoints):
            if singleFit is False:
                return self._MELR(np.column_stack((t[inPoints],y[inPoints],types[inPoints])))
            else:
                return self._singleLR(t[inPoints],y[inPoints])
        else:
            return None
            
    def _MELR(self,data):
        """ Perform mixed-effects regression for a group.
        
            This is split from fitGroup to be able to use it from fitRANSAC
            
            Returns a dictionary with the results
        """
        
        df=pd.DataFrame(data,columns=['TIME', 'OD', 'TYPE'])
        
        #To set that there should be no interaction term
        free=sm.regression.mixed_linear_model.MixedLMParams.from_components(np.ones(2),np.eye(2))
        md = smf.mixedlm('OD ~ TIME', df, groups=df['TYPE'],re_formula='~TIME')
        
        #This warning is shown if the variance in the random slope is too small. It doesn't matter so hide it
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            results = md.fit(free=free)
        
        #Dictionary with the results
        result={}
        result['intercept']=results.params['Intercept']
        result['slope']=results.params['TIME']
        confInt=results.conf_int(0.05)
        result['confInterval']=[confInt[0]['TIME'],confInt[1]['TIME']]
        result['upperLegend']='µ: ' + str(round(result['slope'],3)) + ' [' + str(round(result['confInterval'][0],3)) + ', ' + str(round(result['confInterval'][1],3)) + ']'
        result['lowerLegend']=None
        
        return result
            
    def _singleLR(self,x,y):
        """ Perform linear regression on a single line.
        
            This is split from fitLine to be able to use it from fitRANSAC
            
            Returns a dictionary with the results
        """
        
        model=sm.regression.linear_model.OLS(y,sm.regression.linear_model.add_constant(x))
        results = model.fit()
        
        #Dictionary with the results
        result={}
        result['intercept']=results.params[0]
        result['slope']=results.params[1]
        result['rsquared']=results.rsquared
        result['confInterval']=results.conf_int(0.05)[1,:]
        result['upperLegend']='µ: ' + str(round(result['slope'],3)) + ' [' + str(round(result['confInterval'][0],3)) + ', ' + str(round(result['confInterval'][1],3)) + ']'
        result['lowerLegend']='R-sqr: ' + str(round(result['rsquared'],3))
        
        return result
        
     
    def fitLine(self,index,noRANSAC=False):
        """ Fits a line to a curve and returns the fitting.
        
            Note that the log of the values will be used and that the fitting
            will be done in the interval specified by regressionLimits. This also
            calls on fitRANSAC for a robust fitting.
        """
        
        startT=self._regressionLimits[index,0]
        endT=self._regressionLimits[index,1]
        
        if not np.isnan(startT) and not np.isnan(endT):
            #Get the data
            I=np.where(np.bitwise_and(self._times>=startT, self._times<=endT))
            
            p=np.log(self._values[I,index].flatten(1))
            t=self._times[I]
            
            results=self._singleLR(t,p)
            if noRANSAC is False:
                ransacResults=self._fitRANSAC(t,p,None,results)
                if not ransacResults is None:
                    results['ransac_intercept']=ransacResults['intercept']
                    results['ransac_slope']=ransacResults['slope']
                    results['ransac_rsquared']=ransacResults['rsquared']
                    results['ransac_confInterval']=ransacResults['confInterval']
                    results['ransac_upperLegend']=ransacResults['upperLegend']
                    results['ransac_lowerLegend']=ransacResults['lowerLegend']
                else:
                    results['ransac_intercept']=np.nan
                    results['ransac_slope']=np.nan
                    results['ransac_rsquared']=np.nan
                    results['ransac_confInterval']=[np.nan,np.nan]
                    results['ransac_upperLegend']='No model found'
                    results['ransac_lowerLegend']='No model found'

            self._regressionResults[index]=results
            
    def getRegressionResults(self,indexes):
        """ Create a list of regression results from the indexes."""
        
        tempList=[]
        
        for index in indexes:
            tempList.append(self._regressionResults[index])
       
        return tempList
        
    def setWellLabel(self,index,value):
        """ Set the label of a well."""
        
        if value.count(',')==0 and value.count(';')==0:
            self._wellLabels[index]=value
    
    def setGroupLabel(self,index,value):
        """ Set the label of a group."""
        
        if value.count(',')==0 and value.count(';')==0:
            self._groupLabels[index]=value
    
    def getGroupRegressionResults(self,indexes):
        """ Create a list of regression results from the group indexes."""
        
        tempList=[]
        
        for index in indexes:
            tempList.append(self._groupRegressionResults[index])
       
        return tempList
        
    def saveFile(self,fileName):
        """ Save results to a CSV file."""
        d=self._delimiter
        
        with open(fileName, "w") as csv:
            #Get groups to print
            I=np.where(self.toPlotGroups)[0]
            
            if len(I)>0:
                csv.write('***Groups' + d*8 + '\n')
                csv.write(d*2 + 'mu (1/h)' + d + '95% CI' + d + 'R-sqr' + d + 'mu (1/h) [RANSAC]' + d + '95% CI [RANSAC]' + d + 'R-sqr [RANSAC]' + d + 'Time interval (h)\n')
                
                for index in I:
                    result=self.getGroupRegressionResults([index])[0]
                    limits=self.getGroupRegressionLimits(index)[0]
                    
                    if not result is None:   
                        u='%.3f' % round(result['slope'],3)
                        lCI='%.3f' % round(result['confInterval'][0],3)
                        uCI='%.3f' % round(result['confInterval'][1],3)
                        CI='[' + lCI + ' - ' + uCI + ']'
                        u_r='%.3f' % round(result['ransac_slope'],3)
                        lCI_r='%.3f' % round(result['ransac_confInterval'][0],3)
                        uCI_r='%.3f' % round(result['ransac_confInterval'][1],3)
                        CI_r='[' + lCI_r + ' - ' + uCI_r + ']'
                        lTI='%.3f' % round(limits[0],3)
                        uTI='%.3f' % round(limits[1],3)
                        TI='[' + lTI + ' - ' + uTI + ']'
                        
                        csv.write(self.groupLabels[index] + d*2 + u + d + CI + d*2 + u_r + d + CI_r + d*2 + TI + '\n') 
                    else:
                        csv.write(self.groupLabels[index] + d*8 + '\n')
                    
                    #Then print each well in the group
                    J=np.intersect1d(np.where(self.toPlot)[0],self.getGroupMembers(index))
                    for index in J:
                        result=self.getRegressionResults([index])[0]
                        limits=self.regressionLimits
                        if not result is None:
                            u='%.3f' % round(result['slope'],3)
                            lCI='%.3f' % round(result['confInterval'][0],3)
                            uCI='%.3f' % round(result['confInterval'][1],3)
                            CI='[' + lCI + ' - ' + uCI + ']'
                            R2='%.3f' % round(result['rsquared'],3)
                            u_r='%.3f' % round(result['ransac_slope'],3)
                            lCI_r='%.3f' % round(result['ransac_confInterval'][0],3)
                            uCI_r='%.3f' % round(result['ransac_confInterval'][1],3)
                            CI_r='[' + lCI_r + ' - ' + uCI_r + ']'
                            R2_r='%.3f' % round(result['ransac_rsquared'],3)
    
                            csv.write(d + self.wellLabels[index] + d + u + d + CI + d + R2 + d + u_r + d + CI_r + d + R2_r + d +'\n') 
                        else:
                            csv.write(d + self.wellLabels[index] + d*7 + '\n') 
                            
                    csv.write(d*8 + '\n')
                
            #Get wells to print
            I=np.where(np.bitwise_and(self.toPlot,~self.inGroup))[0]
            if len(I)>0:
                csv.write('***Wells' + d*5 + '\n')
                csv.write(d + 'mu (1/h)' + d + '95% CI' + d + 'R-sqr' + d + 'mu (1/h) [RANSAC]' + d + '95% CI [RANSAC]' + d + 'R-sqr [RANSAC]' + d + 'Time interval (h)' + d + '\n') 
                for index in I:
                    result=self.getRegressionResults([index])[0]
                    limits=self.regressionLimits
                    if not result is None:
                        u='%.3f' % round(result['slope'],3)
                        lCI='%.3f' % round(result['confInterval'][0],3)
                        uCI='%.3f' % round(result['confInterval'][1],3)
                        CI='[' + lCI + ' - ' + uCI + ']'
                        R2='%.3f' % round(result['rsquared'],3)
                        u_r='%.3f' % round(result['ransac_slope'],3)
                        lCI_r='%.3f' % round(result['ransac_confInterval'][0],3)
                        uCI_r='%.3f' % round(result['ransac_confInterval'][1],3)
                        CI_r='[' + lCI_r + ' - ' + uCI_r + ']'
                        R2_r='%.3f' % round(result['ransac_rsquared'],3)
                        lTI='%.3f' % round(limits[index,0],3)
                        uTI='%.3f' % round(limits[index,1],3)
                        TI='[' + lTI + ' - ' + uTI + ']'

                        csv.write(self.wellLabels[index] + d + u + d + CI + d + R2 + d + u_r + d + CI_r + d + R2_r + d + TI + d +'\n') 
                    else:
                        csv.write(self.wellLabels[index] + d*8 + '\n')
     
    def loadFile(self,fileName):
        """ Load a CSV file."""
        
        #Clear any current variables and set them to their default values
        self.initVariables()
        
        #The issue here is that some Biolector files are semicolon separated with
        #decimal comma and some are comma separated with decimal dot. First try to figure
        #out the delimiter by reading the first line and checking for existance of comma or semicolon
        self._delimiter=None
        with open(fileName, 'rb') as csvfile:
            row=csvfile.next()
            commas=row.count(',')
            semicolons=row.count(';')
            
            if commas==1 and semicolons==0:
                self._delimiter=','
            if semicolons==1 and commas==0:
                self._delimiter=';'
            
        #Could not get delimiter, return without error message for now
        if self._delimiter is None:
            return
        
        with open(fileName, 'rb') as csvfile:
            csvreader = csv.reader(csvfile,delimiter=self._delimiter)
            
            #First search to the row where the third row is "TIME [h] ->"
            breakEarly=False
            for row in csvreader:
                if breakEarly is False:
                    if len(row)>=4:
                        if row[3]=='TIME [h] ->':
                            #The current format uses "," as decimal point. This should be checked more carefully
                            self._times=np.zeros(len(row)-4)
                            for i in range(4,len(row)):
                                self._times[i-4]=float(row[i].replace(',','.'))
                                
                            #The Biolector file format may sometimes miss the last measured value for
                            #some wells. This is probably when the program has been aborted prematurely.
                            #Trim all measurements to the shortest sample
                            
                            #Then read the remainder of the values into the value matrix. Only read 48 rows for now (first channel)
                            self._values=np.empty([len(self._times),0])
                            counter=0
                            for row in csvreader:
                                counter=counter+1
                                if counter<=48:
                                    #First convert the values in the row
                                    newRow=np.zeros(len(row)-4)
                                    for i in range(4,len(row)):
                                            newRow[i-4]=float(row[i].replace(',','.'))
                                    
                                    #This means that this row is shorter then the others. Trim old values        
                                    if len(newRow)<len(self._times):
                                        self._times=self._times[0:len(newRow)]
                                        self._values=self._values[0:len(newRow),:]
                                    self._values=my.cat(self._values,newRow[0:len(self._times)],1)
                                else:
                                    breakEarly=True
                                    break
        
        #Normalize values to start at 0. This is problematic if the real OD at t0 is a significant fraction of the
        #OD used for fitting. Add 0.5% of max value for less noise at low levels
        for i in range(0,self._values.shape[1]):
            self._values[:,i]=self._values[:,i]-min(self._values[:,i])
            self._values[:,i]=self._values[:,i]+0.005*max(self._values[:,i])

    def toggleToPlot(self,index):
        """ Toggle whether to plot a well or not."""
        
        self._toPlot[index]=np.logical_not(self._toPlot[index])

    def toggleToPlotGroup(self,index):
        """ Toggle whether to plot a group or not."""
        
        self._toPlotGroups[index]=np.logical_not(self._toPlotGroups[index])
        
    def addToGroup(self,groupIndex,wellIndex):
        """ Add a single well to a group."""
        
        if self._inGroup[wellIndex]==False:
            self._inGroup[wellIndex]=True
            self._groupMembers[groupIndex]=my.cat(self._groupMembers[groupIndex],np.array([wellIndex]))
        
    def getGroupMembers(self,groupIndex):
        """ Get the wells in a given group."""
        return self._groupMembers[groupIndex]
        
    def getGroupRegressionLimits(self,groupIndex):
        """ Get the regression limit for a group. np.nan is used if not set."""
        return self._groupRegressionLimits[groupIndex,:][None,:]
        
    def getGroupColor(self,groupIndex):
        """ Get the color for a group. This is currently the color for the first
            member of the group, but that may change.
            
            Returns both an RGBA array and an gdk.Color object
        """

        members=self._groupMembers[groupIndex]
        if len(members)>0:
            color=self._wellColors[members[0],:][None,:]
            return (color,gtk.gdk.Color(color[0,0],color[0,1],color[0,2]))
        else:
            return (None, None)
                
    def newGroup(self):
        """ Create a new group."""
        if not self._groupLabels is None:
            self._groupLabels.append('Group '+ str(self._groupCounter))
            self._toPlotGroups.append(True)
            self._groupMembers.append(np.zeros(0))
            nan=np.empty((1,2))
            nan[:]=np.nan
            self._groupRegressionLimits=my.cat(self._groupRegressionLimits,nan,0)
            self._groupRegressionResults.append(None)
            
        else:
            self._groupLabels=['Group '+ str(self._groupCounter)]
            self._toPlotGroups=[True]
            self._groupMembers=[np.zeros(0)]
            self._groupRegressionLimits=np.empty((1,2))
            self._groupRegressionLimits[:]=np.nan
            self._groupRegressionResults=[None]
            
        self._groupCounter=self._groupCounter+1
        
    def toggleMultipleToPlot(self,index=None,type=None):
        """ Toggle whether to plot a whole row/column or not.
        
            type=0: index is a row
            type=1: index is a column
            
            index is None: toggle all wells
        """
        
        #To convert between indexes first make a boolean matrix
        mat=np.zeros(self._plateDim)
        
        if not index is None:
            #Toggle row
            if type==0:
                mat[index,:]=True
            else:
                mat[:,index]=True
        else:
            mat[:,:]=True #Toggle all
            
        #Get indexes to toggle
        I=np.where(mat)
        J=np.ravel_multi_index(I, self._plateDim)
        
        if np.any(self._toPlot[J]):
            self._toPlot[J]=False
        else:
            self._toPlot[J]=True
        
if __name__ == "__main__":
    """ Run the program."""
    GetGrowth().showGUI()
