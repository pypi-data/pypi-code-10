#Author: liuliu

import logging, re, os.path, StringIO, itertools
from ConfigParser import SafeConfigParser
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from pylab import plot,show
from analytics_engine import windowlizeChannel
import glob
from time import time
import re


def get_whole(fName):
    '''
    automate the process of 1-5 section dividing.
    '''
    start = time()

    #fName = 'cpt1_Ryan_Dungey.TXT'
    subject_num = fName.split('.')[0]
    '''
    fNames =glob.glob('*.TXT')
    for fName in fNames:
        pattern = re.compile(r'([^\_]+).TXT')
        match = pattern.match(headerName)
        subject_num =  int(match.group(2))
    '''
    lines = None
    with open(fName,'r') as f:
        for line in f:
            if lines is None:
                lines = [[item] for item in line.split()]
            else:
                for i in xrange(len(line.split())):
                    lines[i].append(line.split()[i])
    data = lines
    data = np.array(data)
    data = data.astype(float)
    print 'read data finished. ',time()-start
    start = time()
    #now we need to get the exact cpt section
    cpt_data = data
    whole = [windowlizeChannel(w,sampleRate=256) for w in cpt_data]
    pickle.dump(whole,open('../prowffts/whole_'+str(subject_num)+'.wfft','w'))
    print 'saving whole finished.',str(subject_num),time()-start


def main(fName):
    '''
    automate the process of 1-5 section dividing.
    '''
    start = time()

    #fName = 'cpt1_Ryan_Dungey.TXT'
    subject_num = fName.split('.')[0]
    '''
    fNames =glob.glob('*.TXT')
    for fName in fNames:
        pattern = re.compile(r'([^\_]+).TXT')
        match = pattern.match(headerName)
        subject_num =  int(match.group(2))
    '''
    lines = None
    with open(fName,'r') as f:
        for line in f:
            if lines is None:
                lines = [[item] for item in line.split()]
            else:
                for i in xrange(len(line.split())):
                    lines[i].append(line.split()[i])
    data = lines
    data = np.array(data)
    data = data.astype(float)
    print 'read data finished. ',time()-start
    start = time()
    #now we need to get the exact cpt section
    cpt_data = data
    print 'chopping cpt data finished. ',time()-start
    start = time()
    #now we need to divide up the cpt interval, we know there are 5.
    interval_times = [int(len(cpt_interval_data)/5) for cpt_interval_data in cpt_data]
    easy1 = [cpt_data[i][0:interval_times[i]] for i in xrange(len(cpt_data))]
    easy2 = [cpt_data[i][interval_times[i]:2*interval_times[i]] for i in xrange(len(cpt_data))]
    hard1 = [cpt_data[i][interval_times[i]*2:interval_times[i]*3] for i in xrange(len(cpt_data))]
    hard2 = [cpt_data[i][interval_times[i]*3:interval_times[i]*4] for i in xrange(len(cpt_data))]
    easy3 = [cpt_data[i][interval_times[i]*4:] for i in xrange(len(cpt_data))]
    print 'dividing cpt data finished. ',time()-start
    start = time()
    #now we need to do rolling window and fft  on those
    easy1_wfft = [windowlizeChannel(e,sampleRate=256) for e in easy1]
    easy2_wfft = [windowlizeChannel(e,sampleRate=256) for e in easy2]
    hard1_wfft = [windowlizeChannel(h,sampleRate=256) for h in hard1]
    hard2_wfft = [windowlizeChannel(h,sampleRate=256) for h in hard2]
    easy3_wfft = [windowlizeChannel(e,sampleRate=256) for e in easy3]
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
    import cPickle as pickle
    pickle.dump(easy1_wfft,open('../prowffts/easy1_'+str(subject_num)+'.wfft','w'))
    pickle.dump(easy2_wfft,open('../prowffts/easy2_'+str(subject_num)+'.wfft','w'))
    pickle.dump(easy3_wfft,open('../prowffts/easy3_'+str(subject_num)+'.wfft','w'))
    pickle.dump(hard1_wfft,open('../prowffts/hard1_'+str(subject_num)+'.wfft','w'))
    pickle.dump(hard2_wfft,open('../prowffts/hard2_'+str(subject_num)+'.wfft','w'))
    print 'write divided window fft data finished. ',time()-start
    start = time()
if __name__ == '__main__':
    import glob
    fNames = glob.glob('*.TXT')
    for fName in fNames:
        main(fName)
