'''
This file is used to read csv file and then come up with clustering result.
This file can also be used to do T-Test on means for athletes or controls.
Main function: Main()
'''
import math
import numpy as np
from analytics_engine import ssCluster
from scipy import stats
from scipy.stats import f_oneway as anova
#read the csv and return a dictionary of
#filename -=> channel -=> pearsonr
#u can also specify which pearsonr to read. Defaults to 2.
def read_csv(fileName,p = 2):
    #Returns a list of lists:
    raw = {}
    with open(fileName,'r') as f:
        for line in f:
            data = line.split(',')
            #first comma  is string
            name = data[0]
            #second comma is channel
            channel = data[1]
            #third comma is pearsonr
            pearsonr = data[p]
            #foruth comma is pearsonr for 1,3
            #pearsonr2 = data[3]
            #fifth comma is pearsonr for 2,4
            #pearsonr3 = data[4]
            #p25 = data[5]
            #p34 = data[6]
            #p1324 = data[7]
            if raw.get(name) == None:
                raw[name] = {}
            raw[name][int(channel)]= float(pearsonr)
    return raw
#read in a dictionary of raw and return
#a list of lists of correlations, and the name correspondences.
def raw_transform(raw):
    names = []
    result = []
    max_channels = 0
    for name in raw.keys():
        if name not in names:
            names.append(name)
        #idx is the index of the name from names array
        idx = names.index(name)
        #allocate new space if the name is new.
        if len(result)<idx+1:
            result.append([])
        for channel in sorted(raw[name].keys()):
            result[idx].append(raw[name][channel])
        if max_channels == 0:
            max_channels = len(result[idx])
        else:
            if len(result[idx])<max_channels:
                max_channels = len(result[idx])

    #now we got our result and names,
    #however we need to cut the result to have the same amount of channels.
    for i in xrange(len(result)):
        result[i] = result[i][0:max_channels]
    return result,names
#transform [[1,2,3],[4,5,6]] if 1,2,3 are pro and 4,5,6 are control
#Then return [[1,1,1],[0,0,0]]. Require a names list
def cluster_result_transform(cluster_result,names):
    #currently, if the name length > 3 then pro. Otherwise control.
    for i in xrange(len(cluster_result)):
        for j in xrange(len(cluster_result[i])):
            if len(names[int(cluster_result[i][j])])>3:
                cluster_result[i][j]=1
            else:
                cluster_result[i][j]=0
    return cluster_result

def get_cluster():
    '''
    Read in the csv file and cluster them using
    ssCluster in analytics_engine.

    '''
    raw = read_csv('result2.csv')
    result,names = raw_transform(raw)
    cluster_result = ssCluster(data = np.array(result))
    cluster_result = ssCluster(data = np.array(result),show=False)
    print cluster_result
    cluster_result = cluster_result_transform(cluster_result,names)
    print cluster_result
    return result,names,cluster_result

def transform_cluster(result,names,cluster_result):
    '''
    Apply a sin wave to our result and see which one will make our result better.
    '''
    t = np.linspace(0, len(result[0]), len(result[0]))
    #sinwave
    s = np.sin(2*np.pi*t)
    #s =signal.sawtooth(2*np.pi*t)
    new_result = [item * s for item in result]
    cluster_result = ssCluster(data = np.array(result),show=False)
    print cluster_result
    cluster_result = cluster_result_transform(cluster_result,names)
    print cluster_result

def entropy_test(result,names):
    #transform_cluster(result,names,cluster_result)
    #the pro group channel 1-16
    group_pro = []
    group_all = []
    group_control = []
    for i in xrange(len(names)):
        group_all.extend(result[i])
        if len(names[i])>4:
            group_pro.extend(result[i])
        else:
            group_control.extend(result[i])
    rvs = entropy(group_pro)+entropy(group_control)-entropy(group_all)
    print 'entropy result',rvs



def pro_control_all_ttest(result,names):
    '''
    Compares the pro vs all and control vs all on means
    '''
    group_pro = []
    group_all = []
    group_control = []
    for i in xrange(len(names)):
        group_all.extend(result[i])
        if len(names[i])>4:
            group_pro.extend(result[i])
        else:
            group_control.extend(result[i])
    rvs = anova(group_pro, group_all)
    print 'pro vs all',rvs
    rvs = anova(group_control, group_all)
    print 'control vs all',rvs
def control_channel_test(result,names):
    result = np.array(result)
    group0 = []
    group1 = []
    group2 = []
    group3 = []

    group4 = []
    group5 = []
    group6 = []


    group7 = []
    group8 = []
    group9 = []


    group10 = []
    group11 = []


    group12 = []
    group13 = []
    group14 = []
    group15 = []

    group567=[]
    group8910 = []
    group1112 = []

    #all pro group
    group0_all=result[:,0]
    group1_all=result[:,1]
    group2_all=result[:,2]
    group3_all=result[:,3]

    group4_all=result[:,4]
    group5_all=result[:,5]
    group6_all=result[:,6]

    group7_all=result[:,7]
    group8_all=result[:,8]
    group9_all=result[:,9]

    group10_all=result[:,10]
    group11_all=result[:,11]

    group12_all=result[:,12]
    group13_all=result[:,13]
    group14_all=result[:,14]
    group15_all=result[:,15]

    group567_all = []
    group567_all.extend(group5_all)
    group567_all.extend(group6_all)
    group567_all.extend(group7_all)



    group8910_all=[]
    group8910_all.extend(group8_all)
    group8910_all.extend(group9_all)
    group8910_all.extend(group10_all)

    group1112_all=[]
    group1112_all.extend(group11_all)
    group1112_all.extend(group12_all)

    for i in xrange(len(names)):
        if len(names[i])>=4:
            continue
            #deal with the pros
        group0.append(result[i][0])
        group1.append(result[i][1])
        group2.append(result[i][2])
        group3.append(result[i][3])

        group4.append(result[i][4])
        group5.append(result[i][5])
        group6.append(result[i][6])

        group7.append(result[i][7])
        group8.append(result[i][8])
        group9.append(result[i][9])

        group10.append(result[i][10])
        group11.append(result[i][11])

        group12.append(result[i][12])
        group13.append(result[i][13])
        group14.append(result[i][14])
        group15.append(result[i][15])

        group567.append(result[i][5])
        group567.append(result[i][6])
        group567.append(result[i][7])

        group8910.append(result[i][8])
        group8910.append(result[i][9])
        group8910.append(result[i][10])

        group1112.append(result[i][11])
        group1112.append(result[i][12])

    group0 = np.array(group0)
    rvs = anova(group0, group0_all)
    print 'group0',rvs
    group1 = np.array(group1)
    rvs = anova(group1, group1_all)
    print 'group1',rvs
    group2 = np.array(group2)
    rvs = anova(group2, group2_all)
    print 'group2',rvs
    group3 = np.array(group3)
    rvs = anova(group3, group3_all)
    print 'group3',rvs
    group4 = np.array(group4)
    rvs = anova(group4, group4_all)
    print 'group4',rvs
    group5 = np.array(group5)
    rvs = anova(group5, group5_all)
    print 'group5',rvs
    group6 = np.array(group6)
    rvs = anova(group6, group6_all)
    print 'group6',rvs
    group7 = np.array(group7)
    rvs = anova(group7, group7_all)
    print 'group7',rvs
    group8 = np.array(group8)
    rvs = anova(group8, group8_all)
    print 'group8',rvs
    group9 = np.array(group9)
    rvs = anova(group9, group9_all)
    print 'group9',rvs
    group10 = np.array(group10)
    rvs = anova(group10, group10_all)
    print 'group10',rvs
    group11 = np.array(group11)
    rvs = anova(group11, group11_all)
    print 'group11',rvs
    group12 = np.array(group12)
    rvs = anova(group12, group12_all)
    print 'group12',rvs
    group13 = np.array(group13)
    rvs = anova(group13, group13_all)
    print 'group13',rvs
    group14 = np.array(group14)
    rvs = anova(group14, group14_all)
    print 'group14',rvs
    group15 = np.array(group15)
    rvs = anova(group15, group15_all)
    print 'group15',rvs

    group567 = np.array(group567)
    #group567_all = np.array(group567_all)
    rvs = anova(group567,group567_all)
    print 'group567',rvs

    group8910 = np.array(group8910)
    rvs = anova(group8910,group8910_all)
    print 'group8910',rvs

    group1112 = np.array(group1112)
    rvs = anova(group1112,group1112_all)
    print 'group1112',rvs


    with open('../test.csv','a') as f:
        avg = [group0.mean(),group1.mean(),group2.mean(),group3.mean(),group4.mean(),group5.mean(),group6.mean(),group7.mean(),group8.mean(),group9.mean(),group10.mean(),group11.mean(),group12.mean(),group13.mean(),group14.mean(),group15.mean(),group567.mean(),group8910.mean(),group1112.mean()]
        avg_str = [str(item) for item in avg]
        f.write('control,'+','.join(avg_str)+'\n')

def control_pro_channel_test(result,names):
    result = np.array(result)
    group0 = []
    group1 = []
    group2 = []
    group3 = []
    group4 = []
    group5 = []
    group6 = []
    group7 = []
    group8 = []
    group9 = []
    group10 = []
    group11 = []
    group12 = []
    group13 = []
    group14 = []
    group15 = []

    group567=[]
    group8910 = []
    group1112 = []
    #all pro group
    group0_control = []
    group1_control=[]
    group2_control=[]
    group3_control=[]
    group4_control=[]
    group5_control=[]
    group6_control=[]
    group7_control=[]
    group8_control=[]
    group9_control=[]
    group10_control=[]
    group11_control=[]
    group12_control=[]
    group13_control=[]
    group14_control=[]
    group15_control=[]

    group567_control=[]
    group8910_control = []
    group1112_control = []

    for i in xrange(len(names)):
        if len(names[i])<=4:
            group0_control.append(result[i][0])
            group1_control.append(result[i][1])
            group2_control.append(result[i][2])
            group3_control.append(result[i][3])
            group4_control.append(result[i][4])
            group5_control.append(result[i][5])
            group6_control.append(result[i][6])
            group7_control.append(result[i][7])
            group8_control.append(result[i][8])
            group9_control.append(result[i][9])
            group10_control.append(result[i][10])
            group11_control.append(result[i][11])
            group12_control.append(result[i][12])
            group13_control.append(result[i][13])
            group14_control.append(result[i][14])
            group15_control.append(result[i][15])
            group567_control.append(result[i][5])
            group567_control.append(result[i][6])
            group567_control.append(result[i][7])

            group8910_control.append(result[i][8])
            group8910_control.append(result[i][9])
            group8910_control.append(result[i][10])

            group1112_control.append(result[i][11])
            group1112_control.append(result[i][12])

        else:
            #deal with the pros
            group0.append(result[i][0])
            group1.append(result[i][1])
            group2.append(result[i][2])
            group3.append(result[i][3])
            group4.append(result[i][4])
            group5.append(result[i][5])
            group6.append(result[i][6])
            group7.append(result[i][7])
            group8.append(result[i][8])
            group9.append(result[i][9])
            group10.append(result[i][10])
            group11.append(result[i][11])
            group12.append(result[i][12])
            group13.append(result[i][13])
            group14.append(result[i][14])
            group15.append(result[i][15])

            group567.append(result[i][5])
            group567.append(result[i][6])
            group567.append(result[i][7])

            group8910.append(result[i][8])
            group8910.append(result[i][9])
            group8910.append(result[i][10])

            group1112.append(result[i][11])
            group1112.append(result[i][12])

    group0 = np.array(group0)
    rvs = anova(group0, group0_control)
    print 'group0',rvs
    group1 = np.array(group1)
    rvs = anova(group1, group1_control)
    print 'group1',rvs
    group2 = np.array(group2)
    rvs = anova(group2, group2_control)
    print 'group2',rvs
    group3 = np.array(group3)
    rvs = anova(group3, group3_control)
    print 'group3',rvs
    group4 = np.array(group4)
    rvs = anova(group4, group4_control)
    print 'group4',rvs
    group5 = np.array(group5)
    rvs = anova(group5, group5_control)
    print 'group5',rvs
    group6 = np.array(group6)
    rvs = anova(group6, group6_control)
    print 'group6',rvs
    group7 = np.array(group7)
    rvs = anova(group7, group7_control)
    print 'group7',rvs
    group8 = np.array(group8)
    rvs = anova(group8, group8_control)
    print 'group8',rvs
    group9 = np.array(group9)
    rvs = anova(group9, group9_control)
    print 'group9',rvs
    group10 = np.array(group10)
    rvs = anova(group10, group10_control)
    print 'group10',rvs
    group11 = np.array(group11)
    rvs = anova(group11, group11_control)
    print 'group11',rvs
    group12 = np.array(group12)
    rvs = anova(group12, group12_control)
    print 'group12',rvs
    group13 = np.array(group13)
    rvs = anova(group13, group13_control)
    print 'group13',rvs
    group14 = np.array(group14)
    rvs = anova(group14, group14_control)
    print 'group14',rvs
    group15 = np.array(group15)
    rvs = anova(group15, group15_control)
    print 'group15',rvs
    
    group567 = np.array(group567)
    #group567_all = np.array(group567_all)
    rvs = anova(group567,group567_control)
    print 'group567',rvs

    group8910 = np.array(group8910)
    rvs = anova(group8910,group8910_control)
    print 'group8910',rvs

    group1112 = np.array(group1112)
    rvs = anova(group1112,group1112_control)
    print 'group1112',rvs
    '''
    with open('../test.csv','a') as f:
        avg = [group0.mean(),group1.mean(),group2.mean(),group3.mean(),group4.mean(),group5.mean(),group6.mean(),group7.mean(),group8.mean(),group9.mean(),group10.mean(),group11.mean(),group12.mean(),group13.mean(),group14.mean(),group15.mean(),group567.mean(),group8910.mean(),group1112.mean()]
        avg_str = [str(item) for item in avg]
        f.write('pro,'+','.join(avg_str)+'\n')
    '''

def pro_channel_test(result,names):
    result = np.array(result)
    group0 = []
    group1 = []
    group2 = []
    group3 = []

    group4 = []
    group5 = []
    group6 = []


    group7 = []
    group8 = []
    group9 = []


    group10 = []
    group11 = []


    group12 = []
    group13 = []
    group14 = []
    group15 = []

    group567=[]
    group8910 = []
    group1112 = []

    #all pro group
    group0_all=result[:,0]
    group1_all=result[:,1]
    group2_all=result[:,2]
    group3_all=result[:,3]

    group4_all=result[:,4]
    group5_all=result[:,5]
    group6_all=result[:,6]

    group7_all=result[:,7]
    group8_all=result[:,8]
    group9_all=result[:,9]

    group10_all=result[:,10]
    group11_all=result[:,11]

    group12_all=result[:,12]
    group13_all=result[:,13]
    group14_all=result[:,14]
    group15_all=result[:,15]

    group567_all = []
    group567_all.extend(group5_all)
    group567_all.extend(group6_all)
    group567_all.extend(group7_all)



    group8910_all=[]
    group8910_all.extend(group8_all)
    group8910_all.extend(group9_all)
    group8910_all.extend(group10_all)

    group1112_all=[]
    group1112_all.extend(group11_all)
    group1112_all.extend(group12_all)

    for i in xrange(len(names)):
        if len(names[i])<=4:
            continue
            #deal with the pros
        group0.append(result[i][0])
        group1.append(result[i][1])
        group2.append(result[i][2])
        group3.append(result[i][3])

        group4.append(result[i][4])
        group5.append(result[i][5])
        group6.append(result[i][6])

        group7.append(result[i][7])
        group8.append(result[i][8])
        group9.append(result[i][9])

        group10.append(result[i][10])
        group11.append(result[i][11])

        group12.append(result[i][12])
        group13.append(result[i][13])
        group14.append(result[i][14])
        group15.append(result[i][15])

        group567.append(result[i][5])
        group567.append(result[i][6])
        group567.append(result[i][7])

        group8910.append(result[i][8])
        group8910.append(result[i][9])
        group8910.append(result[i][10])

        group1112.append(result[i][11])
        group1112.append(result[i][12])

    group0 = np.array(group0)
    rvs = anova(group0, group0_all)
    print 'group0',rvs
    group1 = np.array(group1)
    rvs = anova(group1, group1_all)
    print 'group1',rvs
    group2 = np.array(group2)
    rvs = anova(group2, group2_all)
    print 'group2',rvs
    group3 = np.array(group3)
    rvs = anova(group3, group3_all)
    print 'group3',rvs
    group4 = np.array(group4)
    rvs = anova(group4, group4_all)
    print 'group4',rvs
    group5 = np.array(group5)
    rvs = anova(group5, group5_all)
    print 'group5',rvs
    group6 = np.array(group6)
    rvs = anova(group6, group6_all)
    print 'group6',rvs
    group7 = np.array(group7)
    rvs = anova(group7, group7_all)
    print 'group7',rvs
    group8 = np.array(group8)
    rvs = anova(group8, group8_all)
    print 'group8',rvs
    group9 = np.array(group9)
    rvs = anova(group9, group9_all)
    print 'group9',rvs
    group10 = np.array(group10)
    rvs = anova(group10, group10_all)
    print 'group10',rvs
    group11 = np.array(group11)
    rvs = anova(group11, group11_all)
    print 'group11',rvs
    group12 = np.array(group12)
    rvs = anova(group12, group12_all)
    print 'group12',rvs
    group13 = np.array(group13)
    rvs = anova(group13, group13_all)
    print 'group13',rvs
    group14 = np.array(group14)
    rvs = anova(group14, group14_all)
    print 'group14',rvs
    group15 = np.array(group15)
    rvs = anova(group15, group15_all)
    print 'group15',rvs

    group567 = np.array(group567)
    #group567_all = np.array(group567_all)
    rvs = anova(group567,group567_all)
    print 'group567',rvs

    group8910 = np.array(group8910)
    rvs = anova(group8910,group8910_all)
    print 'group8910',rvs

    group1112 = np.array(group1112)
    rvs = anova(group1112,group1112_all)
    print 'group1112',rvs

    with open('../test.csv','a') as f:
        avg = [group0.mean(),group1.mean(),group2.mean(),group3.mean(),group4.mean(),group5.mean(),group6.mean(),group7.mean(),group8.mean(),group9.mean(),group10.mean(),group11.mean(),group12.mean(),group13.mean(),group14.mean(),group15.mean(),group567.mean(),group8910.mean(),group1112.mean()]
        avg_str = [str(item) for item in avg]
        f.write('pro,'+','.join(avg_str)+'\n')
def entropy(l):
    #calulate the entropy of l
    #based entirely on average.
    #steps:
    # 1. transform l into (item-average)^2
    # 2. make sure everything sum up to 1 (redistribution)
    # 3. calculate entropy based on -(sum (pi*log(pi)))
    l = np.array(l)
    l.astype(float)
    #new_l is (the distance to average) ** 2/std
    new_l= (l-l.mean())**2/l.std()
    #probabilities
    new_l = np.array(new_l)
    p = new_l/float(new_l.sum())
    #now p should sum to 1
    print 'sum: ',p.sum()
    print 'IF NOT -1 ERROR'

    #now we cancalculate the entropy
    result = 0
    for item in p:
        #jump over the average == mean items cause they have no entropy
        if item==0:
            continue
        result+=item * math.log(item,2)
    return -1*float(format(result,'.5f'))

def t_test_provscontrol(result,names):
    #transform_cluster(result,names,cluster_result)
    #the pro group
    group1 = []
    #the control group
    group2 = []
    for i in xrange(len(names)):
        if len(names[i])>4:
            #deal with the pros
            group1.extend(result[i])
        else:
            #the control group
            group2.extend(result[i])
    rvs = anova(group1, group2)
    print rvs

def do_tests(p=2):
    raw = read_csv('result2.csv',p=p)
    result,names = raw_transform(raw)
    #entropy_test(result,names)
    print 'control'
    control_channel_test(result,names)
    print 'pro'
    pro_channel_test(result,names)
    print 'pro vs control'
    control_pro_channel_test(result,names)
    print 'pro vs control'
    t_test_provscontrol(result,names)
    pro_control_all_ttest(result,names)
    entropy_test(result,names)

if __name__=='__main__':
    do_tests(p=28)
