import matplotlib
matplotlib.use('TKAgg')
from matplotlib.pylab import plot,show
import numpy as np
import math
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import cPickle as pickle

#test is a model for 2 athelets after clustering. 
#test = {0:np.array([[0,1,2,3],[4,5,6,7],[8,9,10]]),1:np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11]])}
#global variables :

#cNumbers is the number of channels for each athelets. 
#for non-edf imports, 19 is the number. 0-18. 
#for edf import, 20 is the number. 0-19. 
#for new data, 16 is the number.
#e.g. cNumbers['Victoria_Azarenka']=19
#e.g. cNumbers['Ryan_Dungey_data']=20
cNumbers = {}
sampleRate = 250
atheletsList1 = ['Victoria_Azarenka','kai_lenny_1','kai_lenny_2','kai_lenny_3','Matt_Poole1','Matt_Poole2','Jaggar_Eaton','travis_pastrana','Tom_Schaar']
atheletsList2 = ['Brain_Vickers_data', 'Daniel_Russell_data', 'Danny_MacAskill_data', 'David_Alvarez_data', 'David_Walsh_data', 'Elliot_Sloan_data', 'Hans_Backe_data', 'Ian_Walsh2_data', 'James_Morillon_data', 'Juan_Agudelo_data', 'Kaya_Turski_data', 'Levi_Lavallee1_data', 'Levi_LaVallee2_data', 'Peter_Redbull_data', 'Rafa_Ortiz1_data', 'Rafa_Ortiz2_data', 'Rafa_Ortiz3_data', 'Robbie_Madison_data', 'Ryan_Dungey_data', 'Steve_Redbull1_data', 'Steve_Sanders2_data', 'Trey_McCalla_data']
funcNames = ['visualizeHeatMap','plotDistanceHeatmap','screePlot_standardize_old','stdStandardizationChannels','ssCluster']
sports = ['cr', 'g', 'c', 'fb', 'c', 'sb', 'fb', 'w', 'sb', 'ss', 's', 'w', 'w', 'w', 'ss', 'w', 'w', 'w', 'w', 'k', 'k', 'k', 'k', 'mr', 'mr', 'mr', 'fb', 'sb', 'rc', 'sb', 'tn']


import warnings

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    def newFunc(*args, **kwargs):
        warnings.warn("Call to deprecated function %s." % func.__name__,category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc




def flatten(list_of_lists):
    '''
    flattens the input list of lists
    Args: 
        list_of_lists: a list of lists. 
    Returns: 
        The flattened list_of_lists. 
    Raises: 
        None. 
    For exmaple: input [[1,2,3],[4,5]]
                 returns [1,2,3,4,5]
    '''
    return [val for sublist in list_of_lists for val in sublist]

def clear():
    '''
    Function to clear screen for testing
    Args: None
    Returns: None
    Raises: None
    '''
    import os
    os.system("clear")

#setting the global variable - channelList
def set_global_cNumbers():
    global cNumbers
    for athelet in atheletsList1:
        cNumbers[athelet] = 19
    for athelet in atheletsList2:
        cNumbers[athelet] = 20
set_global_cNumbers()


import time
class Timer: 
    '''
    Timer class for record actual time. 
    Args:
        start: the start time.clock()
        end: the end time.clock()
        interval: end_time - start_time
    
    '''
    def __enter__(self):
        self.start = time.clock()
        return self
    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

#basic kmeans method for one data. have to provide k. K defaults to 1
#Need Testing
def kMeans(data,k=1):
	#data should be an ndarray type from numpy
    from matplotlib import pyplot as plt
	#computing K-means with the specific 
    centroids,_ = kmeans(data,k);
	#assign each sample to a cluster
    idx,_ = vq(data,centroids)

	#some plotting using numpy's logical indexing
    plot(data[idx==0,0],data[idx==0,1],'ob',data[idx==1,0],data[idx==1,1],'or',data[idx==2,0],data[idx==2,1],'og') # third cluster points
    plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
    show()

def getFftChannel(channel,name='Victoria_Azarenka',host='localhost',database='athelets',tableName='atheletsfft'):
    return None


# a simple function to compute hierarchical cluster on both rows and columns, and plot heatmaps
#needs testing
#this heat map is not what I want. therefore I need to rewrite it. 
def heatmap(dm):
    from scipy.cluster.hierarchy import linkage, dendrogram
    from scipy.spatial.distance import pdist, squareform
    from matplotlib.pyplot import figure

    D1 = squareform(pdist(dm, metric='euclidean'))
    D2 = squareform(pdist(dm.T, metric='euclidean'))
     
    f = figure(figsize=(8, 8))
    
    # add first dendrogram
    #ax1 = f.add_axes([0.09, 0.1, 0.2, 0.6])
    Y = linkage(D1, method='single')
    Z1 = dendrogram(Y, orientation='right')
    #ax1.set_xticks([])
    #ax1.set_yticks([])
    
    # add second dendrogram
    #ax2 = f.add_axes([0.3, 0.71, 0.6, 0.2])
    Y = linkage(D2, method='single')
    Z2 = dendrogram(Y)
    #ax2.set_xticks([])
    #ax2.set_yticks([])
    
    # add matrix plot
    axmatrix = f.add_axes([0.3, 0.1, 0.6, 0.6])
    idx1 = Z1['leaves']
    idx2 = Z2['leaves']
    D = D1[idx1, :]
    D = D[:, idx2]
    im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap='hot')
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])
    return None

#tested
#read single data channel. 
#[optinal] you can supply name, host,database,tableName,userName,passWord.  
#[optional] you can supply datachannel. default datachannel is 0 
def readDataChannel(channel,name='Victoria_Azarenka', host = 'localhost', database='athelets',tableName ='athelets'):
    '''
    input: a channel, a host name, a database name, and a table name 
    '''
    from pandas.io import sql
    from mysql_utilities import createEngine
    engine, neuroData = createEngine(host=host,database=database,tableName=tableName)
    print 'reading channel '+str(channel)+ ' name '+ str(name)+' from db: '+host+'.'+database+'.'+tableName
    df= sql.read_sql("SELECT voltage  FROM "+tableName+" where channel="+str(channel)+" and name= \'"+name+"\'", engine)
    df.columns = [str(channel)]
    return df

#needs testing
#read Data channels from one person. You can use chanelList or just dont specifiy so the program will ask for all channels.
#needs testing. Not really sure its going to be useful. 
def readDataChannels(channelList,name='Victoria_Azarenka', host = 'localhost', database='athelets',tableName ='athelets'):
    return None
        
    
#tested. This is correlation with raw data. 
def corrChannels(channelList=None,name='Victoria_Azarenka'):
    '''
    input: a channel list containing all channel numbers one wants to do correlation job with. 
    output: pearson's corr coefficient. 
    '''
    if channelList is None:
        channelList = cList
    import pandas as pd
    df=readDataChannel(channelList[0])
    print "combining raw channel: "+str(channelList[0])
    for channel in channelList[1:]:
        print "combining raw channel: "+str(channel)
        df = df.join(readDataChannel(channel,name=name))
    return df.corr()


#this function is to visualize a data
#making it look like a heatmap. 
#1. the data type: dictionary of dictionary of numpy array
def visualizeHeatMap(name='Victoria_Azarenka',data=None):
    '''
    this function takes in a name or maybe some database credentials and table names, 
    returns the heat map for that person and visualize it on the screen. 
    The above sounds really easy. damn it . 
    '''
    import matplotlib.pyplot as plt
    import os
    #for each channel, we want to give it different file names. namely name+channelnumber+heatmap.png and then store them in ../fftheatmaps/ folder.  
    if data is None:
        data = windowlizeChannels(name = name)
    #there should be a check here on data's types 
    for channel in data.keys():
        channelData = data[channel]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #now channelData holds the data for the channel.
        #this time we will build a 2-d array to map the colors. 
        #for each channel, the total start time is interval*total key number. 
#therefore we can build a matrix size at freq size vs data. 
        tempArray = np.zeros((len(channelData[channelData.keys()[0]]), len(channelData.keys())))
        for startTime in channelData.keys():
        # startTime will be 0,10,20,30,40,.....
            timeData = channelData[startTime]
            #now timeData should be a 1 dimentional array. 
            timeData = np.fft.fftshift(timeData)
#the magic number 10.0 is the interval
            compressedData = (timeData-timeData.min())/(timeData.max()-timeData.min())
            tempArray[:,startTime/10]=compressedData
            #freq = np.fft.fftshift(np.fft.fftfreq(len(timeData)))
            #so now freq is the x axis, timeData is the y axis, we can plot this. 
            #plt.plot(compressedData+startTime,freq)
        plt.pcolormesh(tempArray[20:40,:],cmap=plt.cm.OrRd)
        plt.colorbar()
        #plt.show(block=False)
        from file_utilities import createFolder
        createFolder('../fftheatmaps/'+name)
        plt.savefig('../fftheatmaps/'+name+'/'+name+str(channel)+'heatmap.png')
        plt.close('all')

#this function is to visualize a data
#making it look like a heatmap. 
#1. the data type: dictionary of dictionary of numpy array
#this function turns the fft data vertically and then put them on the same channel plot. 
#Its not actually a heatmap, more like a line plot for each window. 
def visualizeHeatMap_old(name='Victoria_Azarenka',data=None):
    '''
    this function takes in a name or maybe some database credentials and table names, 
    returns the heat map for that person and visualize it on the screen. 
    The above sounds really easy. damn it . 
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    #for each channel, we want to give it different file names. namely name+channelnumber+heatmap.png and then store them in ../fftheatmaps/ folder.  
    if data==None:
        data = windowlizeChannels(name = name)
    #there should be a check here on data's types 
    for channel in data.keys():
        channelData = data[channel]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #now channelData holds the data for the channel. 
        for startTime in channelData.keys():
        # startTime will be 0,10,20,30,40,.....
            timeData = channelData[startTime]
            #now timeData should be a 1 dimentional array. 
            timeData = np.fft.fftshift(timeData)
#the magic number 10.0 is the interval
            compressedData = (timeData-timeData.min())/(timeData.max()-timeData.min())*10.0
            freq = np.fft.fftshift(np.fft.fftfreq(len(timeData)))
            #so now freq is the x axis, timeData is the y axis, we can plot this. 
            plt.plot(compressedData+startTime,freq)
        plt.grid()
        #plt.show(block=False)
        from file_utilities import createFolder
        createFolder('../linePlot/')
        plt.savefig('../linePlot/'+name+str(channel)+'heatmap.png')
        plt.close('all')

#tested. given a range of channellist, output its corresponding fft combined map. 
#using windowlizeChannel function. 
#modes: setting the mode parameter will filter the raw data. 
#mode 0: full spectrum 
#mode 1: alpha spectrum 8-12 Hz. 
#mode 2: beta spectrum 13-32 Hz. 
#mode 3: gamma spectrum 32-45 Hz. 
#mode 4: delta spectrum 1-3.5Hz. 
#mode 5: theta spectrum 4-7.5Hz. 
#mode 6: Emotion Emotion: 2-1  ,6-4 ,11-9 ,16-14 ,19-18 in alpha and theta (mode 1 and 5) 
#mode 7: Memory 2-1,6-4 ,7-3 on gamma(mode 3)      
#mode 8: Attention 1,2,3,4,5,6,7,8,9,10 - 17 on alpha
#sampleRate is the rate at which samples are collected. Defaults to 250 Hz. 
def windowlizeChannels(name = 'Victoria_Azarenka',channelList=None,interval=60,space=10,mode=0):
    '''
    not sure if I should put it here or in mysql utilities. 
    This step is to process data so it can be stored as windowed slices, and use fft for all different windows. Each person should have multiple windows, like [10-60,20-70,30-80] ....
    '''
    #steps: 1. read from data or database 
    #       2. convert data to numpy array
    #       3. slice numpy array based on time window, return fft for all time windows. 
    #       4. generate heat maps for all of them. 
    if channelList is None:
        channelList = xrange(cNumbers[name])
    channelList = np.array(channelList)
    if mode==8:
        #get numbers 0-16
        channelList = channelList[channelList<17]
    
    import pandas as pd
    #for each channel
    heatMaps = {}
    if mode==6:
        #2-1,6-4,11-9,16-14,19-18
        #0 -> 2-1
        df = readDataChannel(1,name=name)
        datat1 = df[str(1)]
        
        df = readDataChannel(0,name=name)
        datat0 = df[str(0)]

        data0 = abs(datat1-datat0)
        heatMaps[0] = windowlizeChannel(channel=0,name=name,interval=interval,space=space,mode=mode,data=data0)

        #1-> 6-4
        df = readDataChannel(5,name=name)
        datat1 = df[str(5)]
        
        df = readDataChannel(3,name=name)
        datat0 = df[str(3)]

        data0 = abs(datat1-datat0)
        heatMaps[1] = windowlizeChannel(channel=1,name=name,interval=interval,space=space,mode=mode,data=data0)
        
        #2-> 11-9
        df = readDataChannel(10,name=name)
        datat1 = df[str(10)]
        
        df = readDataChannel(8,name=name)
        datat0 = df[str(8)]

        data0 = abs(datat1-datat0)
        heatMaps[2] = windowlizeChannel(channel=2,name=name,interval=interval,space=space,mode=mode,data=data0)
        
        #3-> 16-14
        df = readDataChannel(15,name=name)
        datat1 = df[str(15)]
        
        df = readDataChannel(13,name=name)
        datat0 = df[str(13)]

        data0 = abs(datat1-datat0)
        heatMaps[3] = windowlizeChannel(channel=3,name=name,interval=interval,space=space,mode=mode,data=data0)
        
        #4 -> 19-18
        df = readDataChannel(18,name=name)
        datat1 = df[str(18)]
        
        df = readDataChannel(17,name=name)
        datat0 = df[str(17)]

        data0 = abs(datat1-datat0)
        heatMaps[4] = windowlizeChannel(channel=4,name=name,interval=interval,space=space,mode=mode,data=data0)
        
        
        return heatMaps
    if mode==7:
        #2-1,6-4,11-9,16-14,19-18
        #0 -> 2-1
        df = readDataChannel(1,name=name)
        datat1 = df[str(1)]
        
        df = readDataChannel(0,name=name)
        datat0 = df[str(0)]

        data0 = abs(datat1-datat0)
        heatMaps[0] = windowlizeChannel(channel=0,name=name,interval=interval,space=space,mode=mode,data=data0)

        #1-> 6-4
        df = readDataChannel(5,name=name)
        datat1 = df[str(5)]
        
        df = readDataChannel(3,name=name)
        datat0 = df[str(3)]

        data0 = abs(datat1-datat0)
        heatMaps[1] = windowlizeChannel(channel=1,name=name,interval=interval,space=space,mode=mode,data=data0)
        
        #2-> 7-3
        df = readDataChannel(6,name=name)
        datat1 = df[str(6)]
        
        df = readDataChannel(2,name=name)
        datat0 = df[str(2)]

        data0 = abs(datat1-datat0)
        heatMaps[2] = windowlizeChannel(channel=2,name=name,interval=interval,space=space,mode=mode,data=data0)
        return heatMaps

    for channel in channelList:
        #for each of the heatMaps[channel] it is an array of array containing arrays of windows
        #e.g. [0-60],[10-70] ... [(end-60)-end]
        print 'Windowlizing channel '+str(channel)+' for '+name
        heatMaps[channel] = windowlizeChannel(channel=channel,name=name,interval = interval, space = space,mode=mode)
    #of course you can run loadDataToDB(data,tableName='athletesffts') to import into database
    #after from mysql_utilities import loadDataToDB
    return heatMaps

#as the function name indicates this functino cuts the fft into half. It ignored the fft when there are negative frequency. 
#the input is raw data. 
#this function mimics what the numpy.fft.fft does, but only reports out the frequency and the power with only greater than 0 x values
#returns x,y
def fft(data):
    y = np.fft.fftshift(np.fft.fft(data)) 
    x = np.fft.fftshift(np.fft.fftfreq(len(data)))
    resultY = y[x>0]
    resultX = x[x>0]
    return resultX,resultY

#tested and working. 
#this function takes in a data and then run fft on it. 
#after fft it shows the plot given fft. 
def showPlot(data,channel=0):
    import matplotlib.pyplot as plt
    #fft.fft(data)
    data = np.fft.fftshift(data)
    freq = np.fft.fftshift(np.fft.fftfreq(len(data)))
    
    plt.plot(freq, data)
    plt.show(block=False)
    '''to find the dominant frequency
    threshold = 0.5*max(abs(spectrum))
    mask = abs(spectrum) > threshold
    peaks = freq[mask]
    '''


#tested. 
#assumed data is a key-value pair.
#input: data in dictionary
#output: sorted key listed appended data. 
#e.g. 1-a,b,c 3-c,a,b 2-b,a,c returns a,b,c,b,a,c,c,a,b 
#the dimention of data must be a dictionary of key->list pairs because I used extend here. 
def  combineFfts(data):
    '''
    this function assumes the data is a 2d array and
    the first dimension is channel, and
    the second dimension is fft windows. 
    return a 1d array with fft - channel. 
    the fft is combined for each channel. 
    '''
    result=[]
    for channel in sorted(data.keys()):
        print("combining fft channel "+str(channel))
        channelTemp=[]
        for window in sorted(data[channel].keys()):
            channelTemp.extend(data[channel][window])
        result.append(channelTemp)
    result = np.array(result)
    return result

# i was going to make standardize window first, but the window cannot be standardized without knowing the whole data. 
#generate standardized windows for all channels for one subject.
#the name is defined in name section. defaults to Victoria_Azarenka
#the data inputted is the processed fft data. With 0 cut off
#input data is a dictionary, lets call it dic
#dic[0] is a dictionary of fft windows, containing fft data. 
#dic[1] is the same thing. 
def standardizeWindows(data,name = 'Victoria_Azarenka'):
    result = {}
    #standardize time windows based among all windows in all channels for one person. 
    #for each of the window for each channel, first need to find max and min, then to standardize them just use (value-min)/(max-min) to standardize them to [0-1]
    #skipped checking each window to make sure they have the same length. 
    channels = data.keys()
    startTimes = data[channels[0]].keys()
    _max = 0.0
    _min = 1.0
    _maxArray = {}
    _minArray = {}
    for startTime in startTimes:
        for channel in channels:
            #get the max for this window across all channels. 
            _max = float(max(max(data[channel][startTime]),_max))
            _min = float(min(min(data[channel][startTime]),_max))
        _maxArray[startTime] = _max
        _minArray[startTime] = _min
    for channel in data.keys():
        result[channel]={}
        for startTime in startTimes:
            result[channel][startTime] = np.array(data[channel][startTime])
            result[channel][startTime]-=_minArray[startTime]
            result[channel][startTime]/=(_maxArray[startTime]-_minArray[startTime])
    return result

#input: channel and name
#output: a dictionary of windowed data.with fft operations 
#needs testing
#alpha: 8-12 Hz
#beta: 13-32 Hz
#gamma: 32-45 Hz
#delta 1-3.5Hz
#theta 4-7.5Hz
#modes: setting the mode parameter will filter the raw data. 
#mode 0: full spectrum 
#mode 1: alpha spectrum 8-12 Hz. 
#mode 2: beta spectrum 13-32 Hz. 
#mode 3: gamma spectrum 32-45 Hz. 
#mode 4: delta spectrum 1-3.5Hz. 
#mode 5: theta spectrum 4-7.5Hz. 
#sampleRate is the rate at which samples are collected. Defaults to 250 Hz. 
def windowlizeChannel(data = None,channel=0,interval=60,space=10,name='Victoria_Azarenka',mode=0,sampleRate = 250.0):
    '''
    this is for single channel windowlization. 
    1. read channel data
    2. slice channel data
    3. fft sliced channel data
    4. save back into db..fft 
    '''
    
    import pandas as pd
    import scipy as sp
    import matplotlib.pyplot as pt
    #import matplotlib.pyplot as plt
    if data is None:
        df=readDataChannel(channel,name=name)
    #this assumes that the column name for channel is str(channel).
    #this column naming was done in readDataChannel. 
    #need to change this later to all power. 
        data = df[str(channel)]
    #unless i m mistaken, I dont see any optimization here for read in all data and windowlize them 1 by 1. 
    #if we have 200 in time, then we have 
#[0,60],[10,70],... in a total of 14 windows. 
    #for each of the window, we would want the ffts. 
    windows = {}
    for start in xrange(0,(len(data)-interval),space):
        #now start is the starting point. 
        if start+interval<len(data):
            rawWindow =data[start:start+interval]
            #NOTE:this fft window is already in absolute value
            fftWindow = abs(np.fft.fft(data[start:start+interval]))
            fftFreq = np.fft.fftfreq(interval,1.0/sampleRate)
            if mode==0:
                windows[start]=fftWindow
            elif mode==1:
                mask = [all(tup) for tup in zip(fftFreq>=8,fftFreq<=12)]
                windows[start]=fftWindow[mask]
            elif mode==2:
                mask = [all(tup) for tup in zip(fftFreq>=13,fftFreq<=32)]
                windows[start]=fftWindow[mask]
            elif mode==3:
                mask = [all(tup) for tup in zip(fftFreq>=32,fftFreq<=45)]
                windows[start]=fftWindow[mask]
            elif mode==4:
                mask = [all(tup) for tup in zip(fftFreq>=1,fftFreq<=3.5)]
                windows[start]=fftWindow[mask]
            elif mode==5:
                mask = [all(tup) for tup in zip(fftFreq>=4,fftFreq<=7.5)]
                windows[start]=fftWindow[mask]
            elif mode==6:
                mask1 = [all(tup) for tup in zip(fftFreq>=4,fftFreq<=7.5)] 
                mask2 = [all(tup) for tup in zip(fftFreq>=8,fftFreq<=12)]
                mask1 = np.array(mask1)
                mask2 = np.array(mask2)
                mask = mask1+mask2
                windows[start]=fftWindow[mask]
            elif mode==7:
                mask = [all(tup) for tup in zip(fftFreq>=32,fftFreq<=45)]
                windows[start]=fftWindow[mask]
            elif mode==8:
                mask = [all(tup) for tup in zip(fftFreq>=8,fftFreq<=12)]
                windows[start]=fftWindow[mask]

        #The contents of freq (and thus also peaks) are the frequencies in units of the sampling rate. 
        else:
            break
    return windows

#get cluster is supposed to be the mean though
#can be used as mean to find the distance matrix.and getting the heatmap for that athelet 
def getCluster(name='Victoria_Azarenka'):
    data = windowlizeChannels(name=name)
    std = combineFfts(standardizeWindows(data))
    dis = clusterWindows(data = std,name=name)
    return data,dis

#NOTE: you can use this function to get a single athelet data. 
def plotDistanceHeatmap(name='Victoria_Azarenka',data=None,plotDendrogram=True, dendrogramPath='../dendrograms/',distanceheatmapPath='../distanceheatmaps/', windowedData=True,labels=None):
    '''
    this step is to cluster all the heat maps generated from windows. 
    Ways to cluster: 
    1. kmeans use scree plots to determine k, or use xmeans. 
    However, what variables: 
        a. frequency, power, window 
        this means: for each window, there is a power-frequency spectrum. for each power, there is a frequency. likewise, for each frequency, there is a power. some power has frequency of 0. 
    Args: 
        name -- the name for this data. 
        data -- the data input, supposedly a 2d array. Default: None
        plotDendrogram -- Boolean for determine if dendrograms should be ploted. Default: True
        dendrogramPath -- the path to which dendrogram should be ploted. Default: ../dendrograms/
        distanceheatmapPath -- the path to which distance heatmap should be plotted. Default: ../distanceheatmaps/
        windowedData -- Boolean indicating whether or not the data input is windowlized raw data or not. Defaults to true. 
        labels -- 1-d array of the labels for dendrogram drawing. Default: None
    '''
    import scipy.cluster.hierarchy as hac
    import matplotlib.pyplot as plt
    from scipy.spatial.distance import pdist
    import scipy
    from file_utilities import createFolder
    createFolder(dendrogramPath+'/')
    createFolder(distanceheatmapPath+'/')
    if data is None:
        data = windowlizeChannels(name=name)
    if windowedData:
        data = combineFfts(standardizeWindows(data))
        dis = pdist(data, lambda u, v: np.sqrt(((u-v)**2).sum()))
        dis = scipy.spatial.distance.squareform(dis)
    else:
        dis = data
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #to show the actual distance matrix:
    plt.pcolormesh(dis)
    #plt.show(block=False)
    plt.colorbar() 
    plt.savefig(distanceheatmapPath+'/heatmap_'+name+'.png')
    plt.close('all')
    if plotDendrogram:
        fig = plt.figure()
        ax=fig.add_subplot(111)
        z = hac.linkage(dis,method='single')
        #if the lables are provided, then return lables. 
        if labels is None:
            hac.dendrogram(z)
        else:
            hac.dendrogram(z,labels = labels)
        #plt.show(block=False)
        plt.savefig(dendrogramPath+'/'+name+'.png')
        plt.close('all')
    return dis

#creating scree plot for each athelets. 
#uses the square distance between each points with its center and sum up to see the scree plot.
#did not use BIC method. 
def screePlot_standardize_old(name='Victoria_Azarenka',data=None,whiten=True):
#    the data is supposed to be a matrix of all channels of the powers. 
    from scipy.cluster.vq import whiten
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)

    X=[]
    Y=[]
    if data is None:
        data = windowlizeChannels(name=name)
    #now the std is the standardized version of data. 
    std = combineFfts(standardizeWindows(data))
    if whiten:
        std2 = whiten(std)
        suffix = 'whitened_'
    else:
        std2 = std
        suffix = 'nowhiten'
    for clusterNumber in range(2,len(std2)):
        centroids,distortion = kmeans(std2,clusterNumber,100)
        X.append(clusterNumber)
        Y.append(distortion)

    plt.plot(X,Y)
    for x,y in zip(X, Y):                        
        ax.annotate(
                '(%s, %s)' % (x,y), 
                xy = (x,y),
                xytext=(0,-10),
                textcoords='offset points',
                ha='center',
                va='top'
                )
    plt.grid()
    #plt.show(block=False)
    from file_utilities import createFolder
    createFolder('../original_standardized_screeplots')
    plt.savefig('../original_standardized_screeplots/'+suffix+name+'.png')
    plt.close('all')

#creating scree plot for each athelets. 
#uses the square distance between each points with its center and sum up to see the scree plot.
#did not use BIC method. 
def screePlot(name=None,data=None,path=None,whiten=False):
    #remember to check if the name and data has the same nullity. They cannot be both not null
    if name is None:
        name='Victoria_Azarenka'
        print 'screePlot: using default name '+name
    if path is None:
        path = '../screeplots/'
        print 'screePlot: using default path '+path
    from file_utilities import createFolder
    createFolder(path)
    
    if not whiten:
        suffix = 'nowhiten_'
    else:
        suffix = 'whitened_'
#    the data is supposed to be a matrix of all channels of the powers. 
    from scipy.cluster.vq import whiten
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    X=[]
    Y=[]
    if data is None:
        data = windowlizeChannels(name=name)
    if type(data) != type(np.array([])):
        std2 = combineFfts(data)
    else:
        std2 = data
    if whiten:
        std2 = whiten(std2)
    #now the std is the standardized version of data. 
    for clusterNumber in range(2,len(std2)):
        centroids,distortion = kmeans(std2,clusterNumber)
        X.append(clusterNumber)
        Y.append(distortion)

    plt.plot(X,Y)
    for x,y in zip(X, Y):                        
        ax.annotate(
                '(%s, %s)' % (x,y), 
                xy = (x,y),
                xytext=(0,-10),
                textcoords='offset points',
                ha='center',
                va='top'
                )

    plt.grid()
    #plt.show(block=False)
    plt.savefig(path+suffix+name+'.png')
    plt.close('all')


#this function uses std as method. Namely, (original value-mean)/standard_deviation applied coordinate-wise.
#this is a helper function for stdStandardization, different from standardizeWindows because it does not standardize time windows based among all windows for each channel for one person. 
def stdStandardizeWindows(data):
    result={}
    channels = data.keys()
    startTimes = data[channels[0]].keys()
    for channel in data.keys():
        result[channel]={}
        for startTime in startTimes:
            result[channel][startTime] = np.array(data[channel][startTime])
            tempMean = result[channel][startTime].mean()
            tempStd = result[channel][startTime].std()
            result[channel][startTime]-=tempMean
            result[channel][startTime]/=tempStd
    return result

#this method assumes the data is a dictinary and needs to be combined first. 
def stdStandardizeChannels(data):
    data = combineFfts(data)
    for i in xrange(len(data)):
        data[i,:]=data[i,:]-data[i,:].mean()
    return data



#this method calculates the (original value - mean)/standard deviation; these are applied coordinate-wise. 
def stdStandardizationWindows(name='Victoria_Azarenka',data=None):
    path = '../stdWindowScreePlots/'
    from file_utilities import createFolder
    createFolder(path)
    if data is None:
        data = windowlizeChannels(name=name)
    std = stdStandardizeWindows(data)
    screePlot(name=name,data=std,path=path,whiten=True)
    screePlot(name=name,data=std,path=path,whiten=False)
    return None

#this method calculates the original value - mean / std evaluation on each channel
def stdStandardizationChannels(name='Victoria_Azarenka',data=None):
    path = '../stdChannelScreePlots/'
    from file_utilities import createFolder
    createFolder(path)
    if data is None:
        data = windowlizeChannels(name=name)
    std = stdStandardizeChannels(data)
    screePlot(name=name,data=std,path=path,whiten=True)
    screePlot(name=name,data=std,path=path,whiten=False)
    return None


#given 2 tuples, return the squared distance between them. 
def dis(a,b):
    return (a[0]-b[0])**2+(a[1]-b[1])**2


#this comment should be put somewhere else. 
#the data return type will be a dictionary of athelet number -> numpy array of clustered channels. 
#Steps followed: 
#for each cthelets
#1. keep on adding cluster until ss cluster reutn 0.1 * previous distance. 
#2. seperate the channels based on the centroids. 
#3. put the channels in one numpy array
#4. put the numpy array in the main dictionary
#Example: if I have athelets 0 and 1
#return is  = {0:np.array([[0,1,2,3],[4,5,6,7],[8,9,10]]),1:np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11]])}
# and this return indicates there are 2 athelets, and athelet0 has 3 clusters while athelet2 has 4. They also have different channel numbers, some number present in 0, some dont. 


#athelet_cluster_distance, takes in the cluster dicitonary, returns the distance map of different athelets. 
#This data is a dictionary of name->clusterings. 
#The clustering is a list of lists, for clustered channels. 
#test = {0:np.array([[0,1,2,3],[4,5,6,7],[8,9,10]]),1:np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11]])}
def athelet_cluster_distance(dendrogramPath='..',dName='athelet_cluster'):
    #now we are getting the jaccard distance between athelets
    data = pickle.load(open('allData.dat','r'))
    dist,names = athelet_pair_jaccard(data)
    #normalize each row to make them real distance matrix
    dist = jacc2disMat(dist)
    #make dendrogram to see the connection
    import scipy.cluster.hierarchy as hac
    import matplotlib.pyplot as plt
    from scipy.spatial.distance import pdist
    import scipy
    from file_utilities import createFolder
    fig = plt.figure()
    ax = fig.add_subplot(111)
    z = hac.linkage(dist,method='single')
    names_new = [name.split('_')[0][0]+name.split('_')[1][0] for name in names]
    hac.dendrogram(z)
    #hac.dendrogram(z,labels=names)
    plt.savefig(dendrogramPath+'/'+dName+'.png')
    return names 





# given l1 as keys and l2 as items. 
# return 1 to 1 value pair as a dictionary
def list2dic(l1,l2=None):
    if l2 is None:
        l2 = range(len(l1))
    result = {}
    curr=0
    for key in l1:
        result[key]= l2[curr]
        curr+=1
    return result



# test = {0:np.array([[0,1,2,3],[4,5,6,7],[8,9,10]]),1:np.array([[0,1,2],[3,4,5],[6,7,8],[9,10,11]])}
#calculate the distance of each channel across athelets. Then return a distance map for visualization. 
#its using a helper method called cross_athelets_pair_jaccard_dis
def cross_athelets_channelDistanceMap(channelClusterDic):
    #step1: find all channels
    channels = set([])
    for athelet in channelClusterDic:
        for cluster in channelClusterDic[athelet]:
            for channel in cluster:
                channels.add(channel)
    #so now we have all channels. if using 0,1 example we now have 0-11
    #step2: create empty numpy array. 
    distances = np.zeros((len(channels),len(channels)))
    #now we have 12 by 12 matrix. can be extended to more elements.  
    for channel1 in xrange(len(channels)):
        for channel2 in xrange(len(channels)):
            temp = cross_athelets_pair_jaccard_dis(channel1,channel2, channelClusterDic)
            distances[channel2][channel1] = temp
    return distances





def cross_athelets_triplet_distanceMap(channelClusterDic):
    channels =set([])
    for athelet in channelClusterDic:
        for cluster in channelClusterDic[athelet]:
            for channel in cluster:
                channels.add(channel)
    distances = {}
    import itertools
    combs = itertools.combinations(range(len(channels)),3)
    for comb in combs:
        channel1 = comb[0]
        channel2 = comb[1]
        channel3 = comb[2]
        temp = cross_athelets_triplet_jaccard_dis(channel1,channel2,channel3,channelClusterDic)
        distances[(channel1,channel2,channel3)] = temp
    return distances

#this is for calculating 1 pair of channels using the clustered channels with different athelets. 
#its using a helper function called inArray
def cross_athelets_pair_jaccard_dis(c1,c2,channelClusterDic):
    '''
    This function is used for calculating the jaccard distance between a pair of channels in one clustering. 
    Args: 
        c1: the first channel
        c2: the second channel
        channelClusterDic: the dictionary containing all the channel clusterings for all different athelets. 
    Returns: 
        A float showing the jacaard distance of c1 and c2
    '''
    #using float point for devision. We want the (1-numerator)/denominator
    
    numerator = 0.0
    denominator = 0.0
    #denominatorChannels = set()
    for athelet in channelClusterDic:
        if inArray(c1,channelClusterDic[athelet]) and inArray(c2,channelClusterDic[athelet]):
            denominator+=1
        for cluster in channelClusterDic[athelet]:
            if c1 in cluster and c2 in cluster:
        #        for channel in cluster:
         #           deominatorChannels.add(channel)
                numerator+=1
    #denominator = sum([len(athlete) for athlete in channelClusterDic.values()])
    return 1.0-numerator/denominator

#this is for caluclating 1 triplet of channels
def cross_athelets_triplet_jaccard_dis(c1,c2,c3,channelClusterDic):
    numerator = 0.0
    denominator = 0.0
    for athelet in channelClusterDic:
        if inArray(c1,channelClusterDic[athelet]) and inArray(c2,channelClusterDic[athelet]) and inArray(c3,channelClusterDic[athelet]):
            denominator+=1
        for cluster in channelClusterDic[athelet]:
            if c1 in cluster and c2 in cluster and c3 in cluster:
                numerator+=1
    return 1.0 - numerator/denominator

#helper function to determine if a number is in an 2d array
#array size does not have to be 2*n it can vary. 
def inArray(n,arr):
    arr= np.array(arr)
    for item in arr:
        if n in item:
            return True
    return False

#helper function to calculate the sswithin/ssbetween clusters
#note the data here is after standardization, combination so it sould be a np array. 
def ss(data,distortion,centroids,clusterNumber):
    if type(data)!= type(np.array([])):
        print('invlaid data type in ss')
        return 0
    ssBetween =0
    for centroid in centroids:
        for centroid2 in centroids:
            ssBetween+=dis(centroid,centroid2)
    ssBetween/=2
    n=len(data)
    pF = (distortion/(clusterNumber-1))/((ssBetween)/(n-clusterNumber))
    return pF

# this is jaccard index. 
def jaccardIndex(l1,l2):
    l1 = set(l1)
    l2 = set(l2)
    n = float(len(l1.intersection(l2)))
    return n/(len(l1)+len(l2)-n)

#jaccardDistance. Does not reply on jaccard index to run
def jaccardDistance(l1,l2):
    n = float(len(l1.intersection(l2)))
    return 1-n/(len(l1)+len(l2)-n)

def dict_flatten(d):
    '''
    :Returns numpy array of flattened dictionary
    '''
    result = []
    for k in sorted(d.keys()):
        result.extend(d[k])
    return np.array(result).astype(float)

#plot the y axis as: pseudo-F = (SS within/(k-1))/(SS between/(n-k)) Here n is the number of records, and k the number of clusters. 
#show is the switch on wheather or not you want to see those screePlots. 
#if you turn show to TRUE, then the ssCLuster is not going to use the threshold 
#if you turn show to False, then the ssCluster will report the result for 1 subject. 
#return is something like: [[2], [0, 1]] a list of lists. 
'''
name: the name of the athelets
data: the windowlized channel of the athelet
path: the path you want the graphs to be put in
whiten: True or False wheather you want the whiten to standardize the data
suffix: The suffix to put at the beginning of each graph file. 
show: True if you just want to see the graphs, False if you dont, and false option also gives you return of clustered channels in a list.
threshold: the threshold to stop adding cluster number
'''
def ssCluster(name='Victoria_Azarenka',data=None,path=None,whiten=False,suffix='',show=True, threshold=0.1,interval=60,space=10,mode=0):
    import matplotlib.pyplot as plt
    from file_utilities import createFolder
    if path is None:
        path = './ssClusterScreePlots/'
    createFolder(path)
    if data is None:
        data = windowlizeChannels(name=name,interval = interval,space=space,mode=mode)
    elif type(data) == type([]) or type(data) == type(np.array([])):
        if type(data[0]) == type({}):
            std2 = np.array([dict_flatten(e) for e in data]).astype(float)
        else:
            std2 = np.array(data).astype(float)
    else:
        std2 = []
        print 'data type:',type(data)
        print 'data is not a valid type, it must be a dictinoary of a list. '
        return
    #std2 = combineFfts(standardizeWindows(data))
    #import pickle
    #pickle.dump(std2,open(str(interval)+'_'+str(space)+'.dump','w'))
    if whiten:
        std2 = whiten(std2)
    X=[]
    Y=[]
    if show:
        print 'show figure in',path
        for clusterNumber in range(2,len(std2)):
            print 'Processing cluster number',clusterNumber
            centroids,distortion = kmeans(std2,clusterNumber,100)
            X.append(clusterNumber)
        #Wait 
        # for sum of squares between clusters, how should I calculate them? e.g. if I have 4 clusters centroids, c1 c2 c3 c4, should i sum square of c1c2, c1c3 c1c4 c2c3 c2c4 c3c4 together?
            ssBetween = 0
            for centroid in centroids:
                for centroid2 in centroids:
                    ssBetween+=dis(centroid,centroid2)
            ssBetween/=2
            n=len(std2)
            pF = (distortion/(clusterNumber-1))/((ssBetween)/(n-clusterNumber))
            Y.append(pF)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(X,Y)
        for x,y in zip(X,Y):
            ax.annotate(
                    '(%s, %s)' % (x,y),
                    xy = (x,y),
                    xytext= (0,-10),
                    textcoords = 'offset points',
                    ha='center',
                    va='top'
                    )
        plt.grid()
        from file_utilities import createFolder
        createFolder(path)
        plt.savefig(path+suffix+name+'.png')
        plt.close('all')
        return None
    else:
        prevDiff = 0
        currDiff=0
        prevss =None
        for clusterNumber in range(2,len(std2)):
            print 'process cluster number',clusterNumber
            centroids,distortion = kmeans(std2,clusterNumber,100)
            if prevss is None:   
                prevss=ss(std2,distortion,centroids,clusterNumber)
                currss = prevss
                prevDiff = 0
                prevCentroids = centroids
            else:
                currss = ss(std2,distortion,centroids,clusterNumber)
                currDiff = currss-prevss
                #if the current difference cannot make it to the threshold, we stop the for loop and report the last cluster number. 
                if -1*currDiff< -1*threshold*prevDiff:
                    centroids = prevCentroids
                    break
                else:
                    prevCentroids = centroids
                    prevss = currss
                    prevDiff = currDiff
        #assign a label of 0-#cluster to all channels. 
        indexes =  vq(std2,centroids)[0] 
        return cross_athelets_orderCluster(indexes)

#suppose we have array([1, 1, 0],'i') and we want it to return [[0,1],[2]] 
def cross_athelets_orderCluster(indexes):
    #check for numpy array
    if type(indexes)!=type(np.array([])):
        return None
    resultGroup = {}
    for channelNum in xrange(len(indexes)):
        if resultGroup.get(indexes[channelNum])!=None:
            resultGroup[indexes[channelNum]].extend([channelNum])
        else:
            resultGroup[indexes[channelNum]] = [channelNum]
    return np.array(resultGroup.values())

#compute the bic for a given distortion
#note this data is not dictionary.Should be an ndarray. 
def bic(data,distortion, clusterNumber):
    import math
    if type(data)!= type(np.array([])):
        print('invalid data type in bic')
        return 0
    return distortion+0.5*math.log(data.size)*clusterNumber*len(data[0])

#compute the aic for a given distortion
#note this data is not a dictionary
def aic(data,distortion, clusterNumber):
    import math
    return distortion+2*clusterNumber*len(data[0])


#BIC method for clustering and visualization
def BICClusters( name='Victoria_Azarenka',data=None):
    path = '../BICClusterScreePlots/'
    #just to make sure the path will be a file name. 
    path+='/'
    from file_utilities import createFolder
    createFolder(path)
    if data is None:
        data = windowlizeChannels(name=name)
    std2 = combineFfts(standardizeWindows(data))
    X=[]
    Y=[]
    for clusterNumber in range(2,len(std2)):
        centroids,distortion = kmeans(std2,clusterNumber)
        X.append(clusterNumber)
        bicTemp = bic(std2,distortion,clusterNumber)
        Y.append(bicTemp)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(X,Y)
    for x,y in zip(X,Y):
        ax.annotate(
                '(%s, %s)' % (x,y),
                xytext= (0,-10),
                textcoords = 'offset points',
                ha='center',
                va='top'
                )
    plt.grid()
    from file_utilities import createFolder
    createFolder(path)
    plt.savefig(path+name+'.png')
    plt.close('all')
    return None

#AIC method for clustering and visualization
def AICClusters( name='Victoria_Azarenka',data=None):
    path = '../AICClusterScreePlots/'
    #just to make sure the path will be a file name. 
    path+='/'
    from file_utilities import createFolder
    createFolder(path)
    if data is None:
        data = windowlizeChannels(name=name)
    std2 = combineFfts(standardizeWindows(data))
    X=[]
    Y=[]
    for clusterNumber in range(2,len(std2)):
        centroids,distortion = kmeans(std2,clusterNumber)
        X.append(clusterNumber)
        aicTemp = aic(std2,distortion,clusterNumber)
        Y.append(bicTemp)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(X,Y)
    for x,y in zip(X,Y):
        ax.annotate(
                '(%s, %s)' % (x,y),
                xy = (x,y),
                xytext= (0,-10),
                textcoords = 'offset points',
                ha='center',
                va='top'
                )
    plt.grid()
    from file_utilities import createFolder
    createFolder(path)
    plt.savefig(path+name+'.png')
    plt.close('all')
    return None


# call 1 function to generate graphs. Using the old athelets with 19 channels. 
def callFunction1(funcName):
    for athelet in atheletsList:
        data = windowlizeChannels(name=athelet)
        globals()[funcName](athelet,data)

#call all functions to generate all graphs and scree plots
#using the new athelets converted from edf having 20 channels
def callFunctions():
    for athelet in atheletsList2:
        with Timer() as t:
            data = windowlizeChannels(name=athelet)
        print('reading athelet %s took %.03f sec.' % (athelet,t.interval))
        for funcName in funcNames:
            with Timer() as t:
                globals()[funcName](athelet,data)
            print('loading function %s took %.03f sec' % (funcName,t.interval))

#call this function to cluster all channels cross athelets using ssCluster, and then returns a heatmap and dendrogram of channels across all athelets. 
def cross_athelets_ssCluster(interval=60,space=10,mode=0,data=None):
    '''
    This function calls ssCluster on all atheletes,
    and returns a dictionary of results. 
    Args:
        interval: int. Represent the interval of time series used. Default: 60
        space: int. Default: 10. Represent the space between windows used. E.g. if interval = 60 and e is 10 then the windows are 0-60, 10-70, 20-80 ...
        mode: int from 0-5 at this moment. Choosing different modes to enable processing different modes. 
        data: the all_atheletes data. If present, then the program will simply calculate the distances between those, and generate the same return 
    Returns: 
        allAthelets, a dictionary of clusterings. 
        File interval_space_mode_allData.dat that contains allAthelets. 
        heatmap and distance for all athelets. heatmap path is 
    Raises:
        Exception: all exception while getting all_athelets. 

    '''
    if data is None:
        allAthelets = {}
    else:
        if type(data) == type({}):
            allAthelets = data
        else:
            print 'data type does not match dictionary. '
            print 'input type: ',type(data)
            return
    try:
        if allAthelets == {}:
            for athelet in atheletsList1:
                with Timer() as t:
                    allAthelets[athelet] = ssCluster(name=athelet,show=False,interval = interval, space = space,mode=mode)
                print('reading athelet %s took %.03f sec.' % (athelet,t.interval))
            for athelet in atheletsList2:
                with Timer() as t:
                    allAthelets[athelet] = ssCluster(name=athelet,show=False,interval = interval, space = space,mode=mode)
                print('reading athelet %s took %.03f sec.' % (athelet,t.interval))
        #visualization in dendrogram and heatmap
        distance = cross_athelets_channelDistanceMap(allAthelets)
        plotDistanceHeatmap(name=str(interval)+'_'+str(space)+'_'+str(mode),data=distance,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData = False,plotDendrogram=True)
    
    except Exception as e:
        print 'exception occured. '
        print e
    finally:
        import cPickle as pickle
        pickle.dump(allAthelets,open(str(interval)+'_'+str(space)+'_'+str(mode)+'_'+'allData.dat','w'))
        return allAthelets
'''
#returns the common clusters based on maximum estimation of cluster. 
#bugs in there. Needs more thoughts on this. 
#this shows nothing. 
#TODO
def athelet_pair_jaccard_clusters(channelClusterDic):
    import numpy as np
    resultDic = {}
    for athelet1 in channelClusterDic.keys():
        resultDic[athelet1]=[]
        for cluster in channelClusterDic[athelet1]:
            clusterTemp = set(cluster)
            for athelet2 in channelClusterDic.keys():
                clusterTemp = clusterTemp.intersection(maxJaccard(channelClusterDic[athelet1],channelClusterDic[athelet2],cluster,returnCluster=True))
            if clusterTemp is not None:
                resultDic[athelet1].append(clusterTemp)
    return resultDic
'''

#uses maxJaccard as helper function
#main function for finding athelet pair jaccard index
#returns the pairwise jaccard index matrix of different athelets. 
#KEEP IN MIND THIS DOES NOT RETURN DISTANCE MATRIX! 
#ITS JACCARD INDEX 
def athelet_pair_jaccard(channelClusterDic):
    '''
    This function is for calculating the athelet pair distance matrix for given channl clustering dictionary. 
    Args: 
        channelClusterDic: a dictionary of channel clustering for each athelets. e.g. {"blake"->[[1,2,3],[4,5],[6,7,8]], "blake2"->[[1,2],[3,4],[5,6,7,8]]}
    Returns: 
       athelets: a list of names of athelets in input.(keys)
       athelet_pair_distances: distance matrix for each pair of athelets
    '''
    athelets = sorted(channelClusterDic.keys())
    athelet_pair_distances = np.zeros((len(athelets),len(athelets)))
    for i in xrange(len(athelets)):
        clustersA = channelClusterDic[athelets[i]]
        for j in xrange(len(athelets)):
            clustersB = channelClusterDic[athelets[j]]
            sum_jaccard = 0.0
            for cluster in clustersA:
                sum_jaccard+=maxJaccard(clustersA,clustersB,cluster)
            athelet_pair_distances[i][j] = sum_jaccard
    count = 0
    for i in xrange(len(athelet_pair_distances)):
        for j in xrange(len(athelet_pair_distances[0])):
            count+=1
            if count>athelet_pair_distances.size/2:
                return athelets,athelet_pair_distances
            athelet_pair_distances[i][j] = (athelet_pair_distances[i][j]+athelet_pair_distances[j][i])/2
            athelet_pair_distances[j][i] = athelet_pair_distances[i][j]


#uses helper function jaccardIndex
#only the channel in the same cluster will give max jaccard
#channelClusterDic -- the dictionary contains all pre-clustered  channels in athelets -> channels fashion
#cluster_in_A is a particular cluster in A. 
#    A = channelClusterDic[athelet1]
#    B = channelClusterDic[athelet2]
def maxJaccard(A,B,cluster_in_A,returnCluster = False):
    #this is a sum for ai 
    #step1: find the cluster where channel is in A. 
    max_jaccard = 0
    max_cluster = None 
    for cluster in B:
        #here we are trying to get value of max_jaccard
        #for the tempDistance I can choose to use either the pair athelet data, or the data cross all thelets. 
        tempJIndex = jaccardIndex(cluster_in_A,cluster)
        if tempJIndex>max_jaccard:
            max_jaccard = tempJIndex
            max_cluster = cluster
    if returnCluster:
        return max_cluster
    else:
        return max_jaccard   


#Not Used any more because this function shows I misunderstood the algorithm
#this is for 2 athelets, A and B
#given channelA from A, return the jaccard index of channelB with channelA. 
def athelet_pair_jaccardIndex(channelA,channelB,A,B):
    numerator = 0.0
    denominator = 0.0
    for cluster in A:
        if channelA in cluster or channelB in cluster:
            denominator+=1
        if channelA in cluster and channelB in cluster:
            numerator+=1
    for cluster in B:
        if channelA in cluster or channelB in cluster:
            denominator+=1
        if channelA in cluster and channelB in cluster:
            numerator+=1
    return numerator/denominator

#NOTE: this id clustering channels, not atheletes. 
#get doublet from file and create heat map and csv ans dendrogram
#needs an infileName as data. 
def get_doublet_from_file_and_create_heatmap_csv_dendrogram(infileName):
    import cPickle as pickle
    from analytics_engine import cross_athelets_channelDistanceMap,plotDistanceHeatmap
    import pickle;
    import csv
    data=pickle.load(open(infileName,'r'));
    distance=cross_athelets_channelDistanceMap(data);
    plotDistanceHeatmap(name='channelsCrossAthelets'+infileName,data=distance,dendrogramPath='../allAthelets/',distanceheatmapPath='../allAthelets/',windowedData = False,plotDendrogram=True)
    from file_utilities import createFolder
    createFolder('../allAthelets/')
    f = open('../allAthelets/channelsCrossAtheletsDis'+infileName+'.csv','w')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerows(distance)
    f.close()
    return distance 

#NOTE: this is clustering channels, not atheletes. 
# same as above, Only different is comparining 3 channels now. 
def get_triplet_from_file_and_create_smalltxt(infileName):
    import pickle
    from analytics_engine import cross_athelets_channelDistanceMap,plotDistanceHeatmap
    import pickle;
    import csv
    #allData.dat
    data=pickle.load(open(infileName,'r'));
    distance=cross_athelets_triplet_distanceMap(data);
    f = open('../allAthelets/channels_triplet_crossAtheletsDis'+infileName+'.csv','w')
    for key in sorted(distance.keys()):
        f.write(str(key)[1:-1]+','+str(distance[key])+'\n')
    f.close()

#this visualizes the jaccard index for each athelets
#this uses helper function athelet_pair_jaccard(data)
#this returns the distance and athelets. Distance is a distance matrix not 0 centric, athelets is the athelet name label
def a_p_jacc_visualize1(data = None,name='athelet_pair',path='../'):
    import pickle
    from analytics_engine import cross_athelets_channelDistanceMap,plotDistanceHeatmap,athelet_pair_jaccard
    import pickle;
    import csv
    if path[-1]!='/':
        path +='/'
    if data is None:
        data=pickle.load(open('allData.dat','r'));
    athelets,distance=athelet_pair_jaccard(data);
    plotDistanceHeatmap(name=name,data=distance,dendrogramPath=path,distanceheatmapPath=path,windowedData = False,plotDendrogram=True) 
    f = open(path+name+'_jaccardIndex.csv','w')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerows(distance)
    f.close()
    f= open(path+name+'_Label.csv','w')
    wr = csv.writer(f,quoting=csv.QUOTE_ALL)
    wr.writerow(athelets)
    f.close()
    return distance,athelets

#a = atheletes
#p = pair
#mode 0: full spectrum 
#mode 1: alpha spectrum 8-12 Hz. 
#mode 2: beta spectrum 13-32 Hz. 
#mode 3: gamma spectrum 32-45 Hz. 
#mode 4: delta spectrum 1-3.5Hz. 
#mode 5: theta spectrum 4-7.5Hz. 
def a_p_jacc_modes(data = None, modes=[1,2,3,5,6,7],name='a_pair',path='../',interval=60,space=10,threshold=1):
    '''
    this function calculates the jacc athelets matrixes using jaccard distance. 
    Args: 
        data: the data dictionary for athelets. defaults: None 
        name: the name to put on the dendrograms Defaults: 1_pair
        modes: the modes that we can use. The modes are listed above the function header for you to choose from, defaults to [1,2,3,5] which are alpha, beta, gamma and theta. 
        path: the path to store the dendrograms and csv for subject names. Defaults: ../
        threshold: At which distance to cut on hierarchical clustering, used for scipy.cluster.hierarchy.fcluster. Defaults:1
    Returns: 
    Raises:
    '''
    import pickle
    t = threshold
    cs =Clusterings()
    allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_allData.dat'))
    #now we have all data for the 0 mode, which is the full spectru, 
    #however, we are not going to pass this in. We need to calculate the distance matrix between pairs of athelets and return a distance matrix. 
    aLabel,dis = athelet_pair_jaccard(allAthelets)
    nick_name=str(0)
    plotDistanceHeatmap(name='jacc_'+nick_name,data=jacc2disMat(dis),dendrogramPath='../atheletsClustering/',distanceheatmapPath='../atheletsClustering/',windowedData=False,plotDendrogram=True,labels=sports)
    #TODO: we can use different linkage methods 
    from scipy.cluster.hierarchy import fcluster,linkage
    #we are going to save space by reusing allAthelets to store the new clustering. 
    #there will only be 1 clustering, therefore we can use a dummy to represent the clustering. 
    allAthelets.clear()
    while fcluster(linkage(dis),t).max()<4:
        t-=0.1
    allAthelets['dummy'] = fcluster2clustering(fcluster(linkage(dis),threshold))
    cs.add(allAthelets,'0')
    for mode in modes:
        t = threshold
        file_name = str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat'
        #nick_name is the shortend name for identify each file
        nick_name = str(mode)
        allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat','r'))
        aLabel,dis = athelet_pair_jaccard(allAthelets)
        #visualize thie dis
        plotDistanceHeatmap(name='jacc_'+nick_name,data=jacc2disMat(dis),dendrogramPath='../atheletsClustering/',distanceheatmapPath='../atheletsClustering/',windowedData=False,plotDendrogram=True, labels=sports)
        allAthelets.clear()
        while fcluster(linkage(dis),t).max()<4:
            t-=0.1
        allAthelets['dummy'] = fcluster2clustering(fcluster(linkage(dis),t))
        cs.add(allAthelets,nick_name)
        #plotDistanceHeatmap(name=str(interval)+'_'+str(space)+'_'+str(mode)+'jacc2',data=dis,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData = False,plotDendrogram=True)
    distance2,labels2 = cs.getJaccMatrix()
    plotDistanceHeatmap(name='All Clusterings_jacc2',data=distance2,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData=False,plotDendrogram=True,labels=labels2)
    #dumpJson(distance2.tolist(),fileName)
    #import os
    #os.system('open index.html')
    return distance2,labels2  

#a = atheletes
#p = pair
#mode 0: full spectrum 
#mode 1: alpha spectrum 8-12 Hz. 
#mode 2: beta spectrum 13-32 Hz. 
#mode 3: gamma spectrum 32-45 Hz. 
#mode 4: delta spectrum 1-3.5Hz. 
#mode 5: theta spectrum 4-7.5Hz. 
def a_p_nmi_modes(data = None, modes=[1,2,3,5,6,7],name='a_pair',path='../',interval=60,space=10,threshold=1):
    '''
    this function calculates the jacc athelets matrixes using jaccard distance. 
    Args: 
        data: the data dictionary for athelets. defaults: None 
        name: the name to put on the dendrograms Defaults: 1_pair
        modes: the modes that we can use. The modes are listed above the function header for you to choose from, defaults to [1,2,3,5] which are alpha, beta, gamma and theta. 
        path: the path to store the dendrograms and csv for subject names. Defaults: ../
        threshold: At which distance to cut on hierarchical clustering, used for scipy.cluster.hierarchy.fcluster. Defaults:1
    Returns: 
    Raises:
    '''
    import pickle
    cs =Clusterings()
    allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_allData.dat'))
    #now we have all data for the 0 mode, which is the full spectru, 
    #however, we are not going to pass this in. We need to calculate the distance matrix between pairs of athelets and return a distance matrix. 
    aLabel,dis = athelet_pair_mig(allAthelets)
    nick_name=str(0)
    plotDistanceHeatmap(name='nmi_'+nick_name,data=jacc2disMat(dis),dendrogramPath='../atheletsClustering/',distanceheatmapPath='../atheletsClustering/',windowedData=False,plotDendrogram=True,labels=sports)
    #TODO: we can use different linkage methods 
    from scipy.cluster.hierarchy import fcluster,linkage
    #we are going to save space by reusing allAthelets to store the new clustering. 
    #there will only be 1 clustering, therefore we can use a dummy to represent the clustering. 
    allAthelets.clear()
    t = threshold
    while fcluster(linkage(dis),t).max()<4:
        t-=0.1
    allAthelets['dummy'] = fcluster2clustering(fcluster(linkage(dis),t))
    cs.add(allAthelets,'0')
    for mode in modes:
        file_name = str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat'
        #nick_name is the shortend name for identify each file
        nick_name = str(mode)
        allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat','r'))
        aLabel,dis = athelet_pair_mig(allAthelets)
        plotDistanceHeatmap(name='nmi_'+nick_name,data=jacc2disMat(dis),dendrogramPath='../atheletsClustering/',distanceheatmapPath='../atheletsClustering/',windowedData=False,plotDendrogram=True,labels=sports)
        allAthelets.clear()
        while fcluster(linkage(dis),t).max()<4:
            t-=0.1
        allAthelets['dummy'] = fcluster2clustering(fcluster(linkage(dis),t))
        cs.add(allAthelets,nick_name)
        plotDistanceHeatmap(name=str(interval)+'_'+str(space)+'_'+str(mode)+'nmi2',data=dis,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData = False,plotDendrogram=True)
    distance2,labels2 = cs.getMigMatrix()
    plotDistanceHeatmap(name='All Clusterings_nmi2',data=distance2,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData=False,plotDendrogram=True,labels=labels2)
    #dumpJson(distance2.tolist(),fileName)
    #import os
    #os.system('open index.html')
    return distance2,labels2     



def fcluster2clustering(data):
    '''
    This function converts the result from fcluster into groups nd array of different groups after using hierechical clustering. 
    Args: 
        data: the returned clustering by fcluster from scipy hierechical clustering. 
    Returns: 
        result: the result clustering using data. 
    Example: 
        data=[12,  4,  6,  4,  2,  9,  8,  2,  7, 12,  4,  1,4,2, 11,  4,  5,2,  1,  2,  4,  2,  3,  4, 11,  3, 13, 14,  4, 10,  4]
        result = 
        [[11, 18], [4, 7, 13, 17, 19, 21], [22, 25], [1, 3, 10, 12, 15, 20, 23, 28, 30], [16], [2], [8], [6], [5], [29], [14, 24], [0, 9], [26], [27]]
        len(result) = 14
    '''
    result = []
    dataDic = {}
    count = 0
    for label in data:
        if dataDic.get(label) is None:
            dataDic[label]=[]
        dataDic[label].append(count)
        count+=1
    for key in dataDic.keys():
        result.append(dataDic[key])
    return result




#NOTE: this visualizes the closest clusters for each athelets
#this algorithm is WRONG and contains bugs, in comparing different athelets
def athelet_pair_visualize_cluster(data = None):
    import pickle
    from analytics_engine import cross_athelets_channelDistanceMap,plotDistanceHeatmap,athelet_pair_jaccard
    import pickle;
    import csv
    if data is None:
        data=pickle.load(open('allData.dat','r'));
    resultDic=athelet_pair_jaccard_clusters(data);
    f = open('../athelet_pair_jaccard_cluster.csv','w')
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    for key,value in resultDic.items():
        wr.writerow([key,value])
    f.close()



#suppose I have a jaccard index matrix and I want to convert it to distance matrx. 
#step1: divide each row and column by the corner point. 
#step2: after dividing, the corner point should be set to 1 because it has the largest jaccard index. 
#step3: for each row and each column, the distance matrix should be 1-that_value. 
#return the distance matrix calculated from jaccard index matrix. 
def jacc2disMat(dis):
    dis = np.array(dis)
    dis = dis.astype(float)
    for i in xrange(len(dis)):
        if dis[i][i]==0:
            continue
        else:
            #maximum jaccard index is at dis[i][i]
            maxJ = dis[i,i]
            dis[i,i:]/=maxJ
            dis[i:,i]/=maxJ
            dis[i,i:] = 1- dis[i,i:]
            dis[i:,i] = 1-dis[i:,i]
            #setting dis[i][i] to be 0
            dis[i,i] = 0
    return dis


def dis2sim(dis):
    '''
    Converts a distance matrix to similarity matrix. 
    A distance matrix is x by x matrix.
    A similarity matrix is x by x matrix.
    Except for the diagonal cells, the similarity matrix is 1 - distance matrix. 
    e.g.
    dis = [
    [0,0.2,0.2],
    [0.2,0,0.2],
    [0.2,0.2,0]
    ]

    sim = [
    [0,0.8,0.8]
    [0.8,0,0.8]
    [0.8,0.8,0]
    ]
    Args: 
        dis --  a 2d-matrix representing the diatnce matrix
        sim -- a 2d-matrix representing the similarity matrix. 
    '''
    dis = np.array(dis)
    dis = dis.astype(float)
    for i in xrange(len(dis)):
        if dis[i][i]==0:
            continue
        else:
            #maximum jaccard index is at dis[i][i]
            dis[i,i:] = 1- dis[i,i:]
            dis[i:,i] = 1-dis[i:,i]
            #setting dis[i][i] to be 0
            dis[i,i] = 0
    return dis.tolist()
#This calculates the mutual information for 2 clusterings. 
#cA: clustering 1
#cB: clustering 2
#returns: a number representing mutual information
#reference: http://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html
#for each cluster in cA a
#for each cluster in cB b
#sum up (a intersect b)/(lena+lenb) * log{(a intersect b)*(lena+lenb)/(lena*lenb)}
#input1: [[0, 1, 2, 6, 7, 11], [17], [3, 4, 5, 8, 9, 10, 12, 13, 14, 15, 16], [18]]
#input2:[[0, 1, 2, 6, 7, 11], [17], [3, 4, 5, 8, 9, 10, 12, 13, 14, 15, 16], [18]]
def mi(cA, cB):
    '''
    Calculates the mutual information between 2 clusters, cA and cB
    Args: 
        cA: list A containing channel information like [[1,2,3],[4,5]]
        cB: list B containing channel information like [[1,2],[3,4,5]]
    Returns: 
        result: float containing mutual information between cA and cB
    Raises: 
        None
    '''
    import math
    result = 0.0
    for a in cA:
        a = set(a)
        for b in cB:
            b= set(b)
            #for testing. If a does not intersect b, then log will not work at all. 
            if len(a&b)==0: 
                continue
            #sum up all p(a,b)log(p(a,b)/p(a)*p(b))
            p_a = float(len(a))/len(flatten(cA))
            #print p_a
            p_b = float(len(b))/len(flatten(cB))
            #print p_b
            p_b_given_a = float(len(a&b))/len(a)
            #print p_b_given_a
            p_a_b = p_a * p_b_given_a 
            #print p_a_b
            result+= p_a_b * math.log(p_a_b/(p_a*p_b),2)     
    return float(format(result,'.5f'))

#this is the mutual information gain for 2 clusters
#using Ig and Mi as dependent functions
def mig(clusterA,clusterB):
    try:
        if mi(clusterA,clusterB)/((ig(clusterA)+ig(clusterB))/2.0)!=mi(clusterB,clusterA)/((ig(clusterB)+ig(clusterA))/2.0):
            print clusterA.tolist()
            print clusterB.tolist()
            print mi(clusterA,clusterB)/((ig(clusterA)+ig(clusterB)/2.0))
            print mi(clusterB,clusterA)/((ig(clusterB)+ig(clusterA)/2.0))
    except:
        print clusterA
        print clusterB
        import sys
        sys.exit(1)
    return mi(clusterA,clusterB)/((ig(clusterA)+ig(clusterB))/2.0)
        

#this calculates the information gain for 1 clustering. 
#e.g. example input would be something like
#[[0, 1, 2, 6, 7, 11], [17], [3, 4, 5, 8, 9, 10, 12, 13, 14, 15, 16], [18]]
#the output should be the information gain from nothing clustered. 
def ig(clustering):
    if type(clustering) != type([]) and type(clustering) != type(np.array([[]])):
        print type(clustering)
        print clustering
        print 'warning: in Ig'
        print 'input not valid as a list' 
        #return 0
    #1. count the number of total channels. 
    #    count the number of each clusters, return a list of nubers. 
    #if using the example input, then the number list shoudl be [6,1,11,1]
    count = 0.0
    numList = []
    for cluster in clustering:
        temp = 0.0
        for item in cluster:
            count+=1.0
            temp+=1.0
        numList.append(temp)
    #this print can make sure the total count and numlist is the correct one
    #print count,numList
    #2. -1 * sum of p(i) log (p(i))
    #now we have total sum in count, we have numlist ready, so 
    #for each element in numlist we get log2(p)*p
    result = 0.0
    
    for el in numList:
        result +=el/count*math.log(el/count,2)
    #dont forget -1*result is the actual result. 
    return -1.0*float(format(result,'.5f'))

#we use the MIg to generate a table for all athelets. 
#basically the formula is: 
#Mutual information(a,b)/0.5*(information gain(a)+information gain(b))
#thisis the mutual information gain, not just the information gain
def athelet_pair_mig(data):
    '''
    The keys are sorted and the output is sorted too. 
    Args: 
        data -- the dictionar of channel clustering 
    Returns:
        Athelets -- the list of keys from original data(sorted)
        athelet_pair_distances -- a 2-d array of distances between passed in keys. 
    '''
    import math
    athelets = sorted(data.keys())
    athelet_pair_distances = np.zeros((len(athelets),len(athelets)))
    for i in xrange(len(athelets)):
        clusterA = data[athelets[i]]
        for j in xrange(len(athelets)):
            clusterB = data[athelets[j]]
            athelet_pair_distances[i][j] = mi(clusterA,clusterB)/((ig(clusterA)+ig(clusterB)/2))
    return athelets,athelet_pair_distances


#now we use the and mig(clustering) to generate the table for all athelets
#and then we can use it to compare different mutual information gain on athelets
#visualize the athelet_pair_mig method. 
def athelet_cluster_mig(data = None,name = 'athelet_pair_mig',path = '..'):
    import pickle
    import csv
    if path[-1]!='/':
        path+='/'
    if data is None:
        data = pickle.load(open('allData.dat','r'))
    athelets,distance = athelet_pair_mig(data)
    #we might need to normalize this distance. 
    plotDistanceHeatmap(name=name,data=distance,dendrogramPath=path,distanceheatmapPath=path,windowedData=False,plotDendrogram=True)
    f = open(path+name+'_mig.csv','w')
    wr = csv.writer(f,quoting=csv.QUOTE_ALL)
    wr.writerows(distance)
    f.close()


#this is a helper function to get all raw data into a pickle dump file. 
#the resulting dump file should be a dictionary of name->raw data. 
#this data is stored for further processing, like selecting specific waves, or subtracting certain waves. 
@deprecated
def dumpAllRaw():
    allAthelets = {}
    for athelet in atheletsList1:
        with Timer() as t: 
            allAthelets[athelet] = windowlizeChannels(name = athelet)
        print('reading athelet %s toko %.03f sec.' %(athelet,t.interval))
    for athelet in atheletsList2:
        with Timer() as t:
            allAthelets[athelet] = windowlizeChannels(name=athelet)
        print('reading athelet %s took %.03f sec'%(athelet,t.interval))
    import pickle
    pickle.dump(allAthelets,open('allRaw.dat','w'))
    return allAthelets

#this function calls the ssCluster function on modes 1-5
def ssCluster_modes():
    for mode in [1,2,3,4,5]:
        cross_athelets_ssCluster(mode=mode)

#interval is the time interval for the slice. 
#space is the space for the slice
#modes is a list of modes that we want this function to read
#this functino visualize all sscluster modes
def nmi_vis(interval=60,space=10,modes=[1,2,3,5],fileName = 'data.json'):
    import pickle
    cs =Clusterings()
    allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_allData.dat'))
    cs.add(allAthelets,'0')
    for mode in modes:
        file_name = str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat'
        #nick_name is the shortend name for identify each file
        nick_name = str(mode)
        allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat','r'))
        distance = cross_athelets_channelDistanceMap(allAthelets)
        cs.add(allAthelets,nick_name)
        plotDistanceHeatmap(name=str(interval)+'_'+str(space)+'_'+str(mode)+'nmi',data=distance,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData = False,plotDendrogram=True)
    distance2,labels2 = cs.getMigMatrix()
    plotDistanceHeatmap(name='All Clusterings_nmi',data=distance2,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData=False,plotDendrogram=True,labels=labels2)
    distance3,labels3 = cs.athelet_mig_matrixes()
    #dumpJson(distance2.tolist(),fileName) 
    #import os
    #os.system('open index.html')
    return distance2,labels2, labels3

#interval is the time interval for the slice. 
#space is the space for the slice
#modes is a list of modes that we want this function to read
#this functino visualize all sscluster modes
def jacc_vis(interval=60,space=10,modes=[1,2,3,5],fileName = 'data.json'):
    import pickle
    cs =Clusterings()
    allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_allData.dat'))
    cs.add(allAthelets,'0')
    for mode in modes:
        file_name = str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat'
        #nick_name is the shortend name for identify each file
        nick_name = str(mode)
        allAthelets = pickle.load(open(str(interval)+'_'+str(space)+'_'+str(mode)+'_allData.dat','r'))
        distance = cross_athelets_channelDistanceMap(allAthelets)
        cs.add(allAthelets,nick_name)
        plotDistanceHeatmap(name=str(interval)+'_'+str(space)+'_'+str(mode)+'jacc',data=distance,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData = False,plotDendrogram=True)
    distance2,labels2 = cs.getJaccMatrix()
    plotDistanceHeatmap(name='All Clusterings_jacc',data=distance2,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData=False,plotDendrogram=True,labels=labels2)
    distance3,labels3 = cs.athelet_jaccard_matrixes()
    #dumpJson(distance2.tolist(),fileName) 
    #import os
    #os.system('open index.html')
    return distance2,labels2,labels3

class Clusterings:
    '''
    This class is for storing all clusterings and compare different clustering methods. 
    The main usage for this class is for getMigMatrix and getJaccMatrix
    Attributes:
        cs: the stored clusterings. for each the mapping is name->clustering, name is the nickname for this clustering, clustering is the actual clustering results. 1
    '''
    def __init__(self):
        #cs is the clustering stored in Clusterings
        self.cs = {}

    #add a new clustering to clusterings, 
    #added the name to the names to the respective position
    def add(self,clustering,name):
        '''
        Args: 
            clustering: a dictionary to be added to the clusterings class. 
            name: string of the input cluctering name
        '''
        if type(clustering) is not type({}):
            raise ValueError('ERROR: in class Clustering: [clustering is not a dictionary]')
        if self.cs.get(name) is not None:
            raise ValueError('ERROR: in class Clustering: [name of clustering aready exists]')
        self.cs[name]=clustering

    #this function gets the distance matrix between the clusterings stored in Clustering class. 
    #it creates a x by x matrix, where x is the total # of our stored clusterings. 
    #it returns the above matrix, filled with numbers by summing up the Mig between different clusterings. 
    #and it returns a second parameter, which is the keys for the index. 
    #the keys can also be retreived from the clustering dictionary itself
    def getMigMatrix(self):
        '''
        Args: Nones
        Returns:
            A 2-d array contains the NMI result for each of the clustering stored in this class. 
            A list contains the names associated with positions in the above 2-d array. 
        Raises:
            ValueError: if there is no clustering availble then a valueError will be raised. 
        '''
        if len(self.cs.keys())==0:
            raise ValueError('ERROR: in class Clustering: [no matrix can be generated -- ]')
        keys = self.cs.keys()
        result  = np.zeros((len(keys),len(keys)))
        for i in xrange(len(keys)):
            for j in xrange(len(keys)):
                cA = self.cs[keys[i]]
                cB = self.cs[keys[j]]
                result[i][j]=np.sum(np.array([mig(cA[tKey],cB[tKey])for tKey in cA.keys()]))
        return result,keys
    #similar to the above, but instead get the jaccard index for clusterings stored in clustering class. 
    #input is none. 
    #outputs the matrix, and the keys for the index. 
    #the key is names of athelets in order of the matrix.
    #e.g. 0->0name, 1->1name, 2->2name.... 
    def getJaccMatrix(self):
        keys = self.cs.keys()
        result = np.zeros((len(keys),len(keys)))
        for i in xrange(len(keys)):
            for j in xrange(len(keys)):
                cA = self.cs[keys[i]]
                cB = self.cs[keys[j]]
                result[i][j]=np.sum(np.array([jaccard(cA[tKey],cB[tKey])for tKey in cA.keys()]))
        return result,keys

    def athelet_mig_matrixes(self):
        '''
         Args: 
            None
        Returns:
            a dictionary of athelet matrixes. 
            Originally we have 31 athelets, therefore we will havea dictionary of 31 matrixes returned, each contatining the distance matrix between different modes. 
            a list of modes used, in order of the matrix
        '''
        result= {}
        #keys contains all athelet names. 
        keys = self.cs[self.cs.keys()[0]].keys()
        for a in keys:
            #for each athelet
            #create a new len(modes) by len(mode) matrix 
            dis = np.zeros((len(self.cs.keys()),len(self.cs.keys())))
            for mode1 in xrange(len(self.cs.keys())):
                for mode2 in xrange(len(self.cs.keys())):
                    dis[mode1][mode2]=mig(self.cs[self.cs.keys()[mode1]][a],self.cs[self.cs.keys()[mode2]][a])
            result[a] = dis
            plotDistanceHeatmap(name='mig_'+a,data=dis,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData=False,plotDendrogram=False)
        return result,self.cs.keys()
    def athelet_jaccard_matrixes(self):
        '''
         Args: 
            None
        Returns:
            a dictionary of athelet matrixes. 
            Originally we have 31 athelets, therefore we will havea dictionary of 31 matrixes returned, each contatining the distance matrix between different modes. 
        '''
        result= {}
        #keys contains all athelet names. 
        keys = self.cs[self.cs.keys()[0]].keys()
        for a in keys:
            #for each athelet
            #create a new len(modes) by len(mode) matrix 
            dis = np.zeros((len(self.cs.keys()),len(self.cs.keys())))
            for mode1 in xrange(len(self.cs.keys())):
                for mode2 in xrange(len(self.cs.keys())):
                    dis[mode1][mode2]=jaccard(self.cs[self.cs.keys()[mode1]][a],self.cs[self.cs.keys()[mode2]][a])
            result[a] = dis
            plotDistanceHeatmap(name='jacc_'+a,data=dis,dendrogramPath='../ChannelClustering/',distanceheatmapPath='../ChannelClustering/',windowedData=False,plotDendrogram=False)
        
        return result,self.cs.keys()

#1. find the closest cluster from b to match with A's cluster. 
#2. sum up the values for all A. 
#3. sum up the 1 for all B. 
#4. add up 2 and 3 and take average, return. 
#e.g. if we have A=[[1,2,3,4],[5,6]] B = [[1,2,3],[4,5,6]]
#then 2 gives us jacc([1,2,3,4][1,2,3])+jacc([5,6],[4,5,6]) = 3/4+2/3
#3 gives us jacc([1,2,3],[1,2,3,4])+jacc([4,5,6],[5,6])=3/4+2/3
def jaccard(clusterA,clusterB):
    result = 0.0
    for cluster in clusterA:
        result+=maxJaccard(clusterA,clusterB,cluster)
    for cluster in clusterB:
        result+=maxJaccard(clusterB,clusterA,cluster)
    return result/2.0

def dumpJson(data,fileName):
    import json
    with open(fileName,'w') as outfile:
        json.dump(data,outfile)

#prepare the matrix good enough for D3 to process. 
#making every row sum up to be 1/len(matrix)
#every value is then converted to the respective ratios. 
#e.g. for a matrix like : [[1,1,1,1,1]] the result matrix should be [[0.2,0.2,0.2,0.2,0.2]]
def prepareMatrix(matrix):
    '''
    Prepares the matrix for chord diagram to use. 
    e.g. input: [[1,1,1,1,1]] then the output should be: [[.2,.2,.2,.2,.2]]
    e.g. input: [[1,1,1,1,1],[1,1,1,1,1]]
         output:[[.2,.2,.2,.2,.2],[.2,.2,.2,.2,.2]]
    Args: 
        matrix -- 2d array containing numbers. 
    Returns: 
        result -- 2d array containig transformed matrix. this matrix has the same dimension as the matrix input. 
    '''
    lineMax = 1.0/len(matrix)
    matrix = np.array(matrix)
    matrix = matrix.astype(float)
    result = [];
    
    for line in matrix: 
        total = 0.0+sum(line)
        line*=1.0
        line/=total
        line*=lineMax
        result.append(line.tolist())
    return result


#process the input matrix
#use jacc2disMat and dis2sim
#output the json file as name indicates
def matrixSim(matrix,name):
    if matrix[0][0] != 0:
        matrix = jacc2disMat(matrix)
    matrix = dis2sim(matrix)
    #matrix = prepareMatrix(matrix)
    import json
    json.dump(matrix,open(name,'w'))
def main(mode='control'):
    #now get the wffts folders from controls. 
    control_wfft_path = "/home/lliu/Athletes/data/Controls/wffts/"
    #for pros: 
    pro_wfft_path = '/home/lliu/Athletes/data/Pros/prowffts/'
    from glob import glob
    fileNames = glob(control_wfft_path+'full*.wfft')
    data = {}
    for fName in fileNames:
        data[fName] = ssCluster(name=fName,data=pickle.load(open(fName,'r')),show=False)
    #so now data is the all_athelets_dict. We can simply put it to cross_athelet_sscluster. 
    cross_athelets_ssCluster(data=data)
if __name__ == '__main__':
    main()

