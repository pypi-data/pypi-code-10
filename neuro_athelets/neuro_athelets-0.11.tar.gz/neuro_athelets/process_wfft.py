import glob
import cPickle as pickle
import numpy as np
from scipy import stats
def dict_flatten(d):
    '''
    :Returns numpy array of flattened dictionary
    '''
    result = []
    for k in sorted(d.keys()):
        result.extend(d[k])
    return np.array(result).astype(float)

#this checks for the first easy and last easy, namely easy1 and easy3, get pearson's correlations
def get_diff(fName = None,result_file=None):
    if result_file is None:
        result_file = '../../../result2.csv'
    groups = ['easy1','easy2','hard1','hard2','easy3']
    if fName is None:
        fName = '_cpt_David_walsh'
    print fName
    easy1 = groups[0]+fName+'.wfft'
    easy2 = groups[1]+fName+'.wfft'
    hard1 = groups[2]+fName+'.wfft'
    hard2 = groups[3]+fName+'.wfft'
    easy3 = groups[4]+fName+'.wfft'

    easy1_data = pickle.load(open(easy1,'r'))
    easy2_data = pickle.load(open(easy2,'r'))
    easy3_data = pickle.load(open(easy3,'r'))
    hard1_data = pickle.load(open(hard1,'r'))
    hard2_data = pickle.load(open(hard2,'r'))
  
    print len(easy1_data)
    print len(easy1_data[0])
    print len(easy1_data[0][0])
    
    easy1_data = [dict_flatten(e) for e in easy1_data]
    easy2_data = [dict_flatten(e) for e in easy2_data]
    easy3_data = [dict_flatten(e) for e in easy3_data]
    hard1_data = [dict_flatten(e) for e in hard1_data]
    hard2_data = [dict_flatten(e) for e in hard2_data]
    
    easy1_data = np.array(easy1_data).astype(float)
    easy2_data = np.array(easy2_data).astype(float)
    easy3_data = np.array(easy3_data).astype(float)
    hard1_data = np.array(hard1_data).astype(float)
    hard2_data = np.array(hard2_data).astype(float)

    if easy1_data.size != easy3_data.size:
        cut_length = len(easy1_data[0])
        cut_easy3_data = [channel[0:cut_length] for channel in easy3_data]
        easy3_data = np.array(cut_easy3_data).astype(float)

    easy1_hard1 = easy1_data - hard1_data
    easy2_hard2 = easy2_data - hard2_data
    #print len(easy3_data)
    #print len(easy3_data[0])
    with open(result_file,'a') as f:
        for i in xrange(len(easy1_data)):
            #pearsonr between easy1 and easy 3
            corr12 = stats.pearsonr(easy1_data[i],easy2_data[i])
            corr13 = stats.pearsonr(easy1_data[i],hard1_data[i])
            corr14 = stats.pearsonr(easy1_data[i],hard2_data[i])
            corr15 = stats.pearsonr(easy1_data[i],easy3_data[i])
            corr23 = stats.pearsonr(easy2_data[i],hard1_data[i])
            corr24 = stats.pearsonr(easy2_data[i],hard2_data[i])
            corr25 = stats.pearsonr(easy2_data[i],easy3_data[i])
            corr34 = stats.pearsonr(hard1_data[i],hard2_data[i])
            corr35 = stats.pearsonr(hard1_data[i],easy3_data[i])
            corr45 = stats.pearsonr(hard2_data[i],easy3_data[i])
            corr1234 = stats.pearsonr(easy1_data[i]-easy2_data[i],hard1_data[i]-hard2_data[i])
            corr1534 = stats.pearsonr(easy1_data[i]-easy3_data[i],hard1_data[i]-hard2_data[i])
            corr1235 = stats.pearsonr(easy1_data[i]-easy2_data[i],hard1_data[i]-easy3_data[i])
            corr1245 = stats.pearsonr(easy1_data[i]-easy2_data[i],hard2_data[i]-easy3_data[i])
            corr1324 = stats.pearsonr(easy1_hard1[i],easy2_hard2[i])
            corr1325 = stats.pearsonr(easy1_data[i]-hard1_data[i],easy2_data[i]-easy3_data[i])
            corr1345 = stats.pearsonr(easy1_data[i]-hard1_data[i],hard2_data[i]-easy3_data[i])
            corr1423 = stats.pearsonr(easy1_data[i]-hard2_data[i],easy2_data[i]-hard1_data[i])
            corr1425 = stats.pearsonr(easy1_data[i]-hard2_data[i],easy2_data[i]-easy3_data[i])
            corr1435 = stats.pearsonr(easy1_data[i]-hard2_data[i],hard1_data[i]-easy3_data[i])
            corr1523 = stats.pearsonr(easy1_data[i]-easy3_data[i],easy2_data[i]-hard1_data[i])
            corr1524 = stats.pearsonr(easy1_data[i]-easy3_data[i],easy2_data[i]-hard2_data[i])
            corr1534 = stats.pearsonr(easy1_data[i]-easy3_data[i],hard1_data[i]-hard2_data[i])
            corr2345 = stats.pearsonr(easy2_data[i]-hard1_data[i],hard2_data[i]-easy3_data[i])
            corr2435 = stats.pearsonr(easy2_data[i]-hard2_data[i],hard1_data[i]-easy3_data[i])
            corr2534 = stats.pearsonr(easy2_data[i]-easy3_data[i],hard1_data[i]-hard2_data[i])
            correh = stats.pearsonr((easy1_data[i]+easy2_data[i]+easy3_data[i])/3,(hard1_data[i]+hard2_data[i])/2)

            #now we dont need the 2-tailed p value.
            #f.write(','.join([fName,str(i),str(corr[0]),str(corr[1])])+'\n')
            f.write(','.join([fName,str(i),\
                    str(corr12[0]),\
                    str(corr13[0]),\
                    str(corr14[0]),\
                    str(corr15[0]),\
                    str(corr23[0]),\
                    str(corr24[0]),\
                    str(corr25[0]),\
                    str(corr34[0]),\
                    str(corr35[0]),\
                    str(corr45[0]),\
                    str(corr1234[0]),\
                    str(corr1534[0]),\
                    str(corr1235[0]),\
                    str(corr1245[0]),\
                    str(corr1324[0]),\
                    str(corr1325[0]),\
                    str(corr1345[0]),\
                    str(corr1423[0]),\
                    str(corr1425[0]),\
                    str(corr1435[0]),\
                    str(corr1523[0]),\
                    str(corr1524[0]),\
                    str(corr1534[0]),\
                    str(corr2345[0]),\
                    str(corr2435[0]),\
                    str(corr2534[0]),\
                    str(correh[0])])\
                    +'\n')
#e12 = (easy1_data + easy2_data)/2
#h12 = (hard1_data + hard2_data)/2

#diff = h12-e12
#pickle.dump(diff,open('../../diff/diff'+fName+'.diff','w'))
fileNames = glob.glob('easy1*.wfft')
fNames = [item.split('.')[0][5:] for item in fileNames]
for fName in fNames:
    get_diff(fName)
