# License: BSD 3-clause
# Author: Boris Reuderink
# Modified: liuliu
 
import logging, re, os.path, StringIO, itertools
from ConfigParser import SafeConfigParser
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from pylab import plot,show
from analytics_engine import windowlizeChannel

#TODO:
# - add encoding of commas (\1)
# - verify units for resolution in UTF8
 
log = logging.getLogger('__main__')
 
def read_header(fname):
  with open(fname) as f:
    linNum =0
    temp = ''
    temp = f.readline().strip()
    while(temp!= 'Brain Vision V-Amp Data Header File Version 1.0'):
        temp = f.readline().strip()
        #temp = f.readline().strip()
        #print temp
        #print "line number: ", linNum
        linNum+=1
        #print "continue?y/n"
        scan= raw_input();
        if scan == 'n' or linNum == 7:
          break
    # setup config reader
   # assert temp == \
    #  'Brain Vision Data Exchange Header File Version 1.0'
 # lines = itertools.takewhile(lambda x: '[Comment]' not in x, f.readlines())
   #interestingly, i think this is wrong. 

    lines = itertools.takewhile(lambda x: 'Comment' not in x, f.readlines())
    lines = ''.join(lines)
    #print lines;
#    sys.exit()

    cfg = SafeConfigParser()
    cfg.readfp(StringIO.StringIO(lines))
 
    # get sampling info
    sample_rate = 1e6/cfg.getfloat('Common Infos', 'SamplingInterval')
    nchann = cfg.getint('Common Infos', 'NumberOfChannels')
 
    log.info('Found sample rate of %.2f Hz, %d channels.' % 
      (sample_rate, nchann))
 
    # check binary format
    assert cfg.get('Common Infos', 'DataOrientation') == 'MULTIPLEXED'
    assert cfg.get('Common Infos', 'DataFormat') == 'BINARY'
    assert cfg.get('Binary Infos', 'BinaryFormat') == 'IEEE_FLOAT_32'
 
    # load channel labels
    chan_lab = ['UNKNOWN'] * nchann
    chan_resolution = np.ones(nchann) * np.nan
    for (chan, props) in cfg.items('Channel Infos'):
      n = int(re.match(r'ch(\d+)', chan).group(1))
      name, refname, resolution, unit = props.split(',')[:4]
 
      chan_lab[n-1] = name
      chan_resolution[n-1] = resolution
 
    # locate EEG and marker files
    eeg_fname = cfg.get('Common Infos', 'DataFile')
    marker_fname = cfg.get('Common Infos', 'MarkerFile')
 
    return dict(sample_rate=sample_rate, chan_lab=chan_lab, 
      chan_resolution=chan_resolution, eeg_fname=eeg_fname, 
      marker_fname=marker_fname)
 
 
def read_eeg(fname, chan_resolution):
	#np.atleast_2d View inputs as arrays with at least two dimensions.
  chan_resolution = np.atleast_2d(chan_resolution)
  nchan = chan_resolution.size
 #read binary file using 'rb' command
  with open(fname, 'rb') as f:
  	#raw is the information read in file. 
    raw = f.read()
    #size is the length of raw divided by 2 because its binary
    size = len(raw)/2
    #ndarray is an n dimensional array. 
    #nchan is the number of channels
    #size/nchan is the time. 
    #ints is the time vs channel vs data array in type <i2 = np.int16 order in column major order and buffer Used to fill the array with data.
    ints = np.ndarray((nchan, size/nchan), dtype=np.int16, order='F', buffer=raw)
    return ints * chan_resolution.T
 
 
def read_markers(fname):
  with open(fname) as f:
    # setup config reader
    assert f.readline().strip() == \
        'Brain Vision Data Exchange Marker File, Version 1.0'
    cfg = SafeConfigParser()
    cfg.readfp(f)
    events = {}
    results = []
    for (marker, info) in cfg.items('Marker Infos'):
        mtype, mdesc, offset, duration, channels = info.split(',')[:5]
        
        mdesc = mdesc.lower().split()
        events[tuple(mdesc)] = offset
    for mdesc in events.keys():
        if 'full' in mdesc and 'cpt' in mdesc and 'start' in mdesc:
            results.insert(0,events[mdesc])
        elif 'test' not in mdesc and 'cpt' in mdesc and 'start' in mdesc:
            results.append(events[mdesc])
    #print events
    if len(results)==0:
        import sys
        print 'ERROR: marker error,no cpt starting time'
        sys.exit(1)
    results = [results[0],int(results[0])+1024*60*20]
    results = np.asarray(results, int)
    results-= 1  # use zero-based indexing
    print results
    print events
    return results
 
def read_data(header_fname, marker_fname=None, eeg_fname=None):
  '''
  Read BrainVision Recorder header file, locate and read the marker and EEG
  file. Returns a header dictionary, a matrix with events and the raw EEG.
  '''
  containing_dir = os.path.split(header_fname)[0]
  header = read_header(header_fname)
 
  if not marker_fname:
    # locate marker file
    marker_fname = os.path.join(containing_dir, header['marker_fname'])
  E = read_markers(marker_fname)
 
  if not eeg_fname:
    # locate EEG file
    eeg_fname = os.path.join(containing_dir, header['eeg_fname'])
  X = read_eeg(eeg_fname, header['chan_resolution'])
 
  return header, E, X
def getNames(s):
    '''
    Read a input name and return a tuple with ahdr amrk and eeg as its extension names. 
    '''
    return (s+'.ahdr',s+'.amrk',s+'.eeg')

def get_whole():
    '''
    automate the process of cpt dividing.
    '''
    import glob
    from time import time
    import re
    start = time()
    headerName =glob.glob('*.ahdr')[0]
    pattern = re.compile(r'([a-zA-Z]+)([0-9]+)')
    match = pattern.match(headerName)
    subject_num =  int(match.group(2))

    header,E,raw_data = read_data(headerName)
    print 'read data finished. ',time()-start
    start = time()
    #now we need to get the exact cpt section
    cpt_interval = E
    print cpt_interval
    cpt_data = [channel_data[cpt_interval[0]:cpt_interval[1]] for channel_data in raw_data]
    cpt_data = np.array(cpt_data)
    print 'chopping cpt data finished. ',time()-start
    whole = [windowlizeChannel(w,sampleRate=1024) for w in cpt_data]
    pickle.dump(whole,open('whole_'+str(subject_num)+'.wfft','w'))
    print 'saving whole finished. ',str(subject_num),time()-start

#temp = getNames('Liu PreTest 11-7-14')
def main():
    '''
    automate the process of 1-5 section dividing.
    '''
    import glob
    from time import time
    import re
    start = time()
    headerName =glob.glob('*.ahdr')[0]
    pattern = re.compile(r'([a-zA-Z]+)([0-9]+)')
    match = pattern.match(headerName)
    subject_num =  int(match.group(2))

    header,E,raw_data = read_data(headerName)
    print 'read data finished. ',time()-start
    start = time()
    #now we need to get the exact cpt section
    cpt_interval = E
    print cpt_interval
    cpt_data = [channel_data[cpt_interval[0]:cpt_interval[1]] for channel_data in raw_data]
    cpt_data = np.array(cpt_data)
    print 'chopping cpt data finished. ',time()-start
    start = time()
    #now we need to divide up the cpt interval, we know there are 5. 
    interval_times = [int(len(cpt_interval_data)/5) for cpt_interval_data in cpt_data]
    full = cpt_data
    easy1 = [cpt_data[i][0:interval_times[i]] for i in xrange(len(cpt_data))]
    easy2 = [cpt_data[i][interval_times[i]:2*interval_times[i]] for i in xrange(len(cpt_data))]
    hard1 = [cpt_data[i][interval_times[i]*2:interval_times[i]*3] for i in xrange(len(cpt_data))]
    hard2 = [cpt_data[i][interval_times[i]*3:interval_times[i]*4] for i in xrange(len(cpt_data))]
    easy3 = [cpt_data[i][interval_times[i]*4:] for i in xrange(len(cpt_data))]
    print 'dividing cpt data finished. ',time()-start
    start = time()
    #now we need to do rolling window and fft  on those 
    full_wfft = [windowlizeChannel(e,sampleRate=1024) for e in full]
    easy1_wfft = [windowlizeChannel(e,sampleRate=1024) for e in easy1]
    easy2_wfft = [windowlizeChannel(e,sampleRate=1024) for e in easy2]
    hard1_wfft = [windowlizeChannel(h,sampleRate=1024) for h in hard1]
    hard2_wfft = [windowlizeChannel(h,sampleRate=1024) for h in hard2]
    easy3_wfft = [windowlizeChannel(e,sampleRate=1024) for e in easy3]
    print 'windowlize fft finished. ',time()-start
    start = time()
    '''
    #############################
    #no longer needed because we have integrated fft in windowlizeChannel function at anlytics engine
    #############################
    #now we need to do fft transform for those 5 windows. 
    easy1_window_fft = window_fft(easy1_window)
    easy2_window_fft = window_fft(easy2_window)
    hard1_window_fft = window_fft(hard1_window)
    hard2_window_fft = window_fft(hard2_window)
    easy3_window_fft = window_fft(easy3_window)
    #now we need to compare 1+2 to 3+4
    '''
    #did i do this wrongly? This is so interesting.
    import cPickle as pickle
    pickle.dump(full_wfft,open('full_'+str(subject_num)+'.wfft','w'))
    pickle.dump(easy1_wfft,open('easy1_'+str(subject_num)+'.wfft','w'))
    pickle.dump(easy2_wfft,open('easy2_'+str(subject_num)+'.wfft','w'))
    pickle.dump(easy3_wfft,open('easy3_'+str(subject_num)+'.wfft','w'))
    pickle.dump(hard1_wfft,open('hard1_'+str(subject_num)+'.wfft','w'))
    pickle.dump(hard2_wfft,open('hard2_'+str(subject_num)+'.wfft','w'))
    print 'write divided window fft data finished. ',time()-start
    start = time()
 
if __name__ == '__main__':
    main()
