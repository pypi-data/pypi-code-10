# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 22:50:14 2014

@author: Fujitsu
"""
def rsquared(x, y):
    import scipy
    """ Return R^2 where x and y are array-like."""
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2
    
def PRESS(ArrayYpred):
    import numpy as np
    ncol = ArrayYpred.shape[1]
    SeriesPRESS = []
    for i in range(1,ncol):
        SE = (ArrayYpred[:,i] - ArrayYpred[:,0])**2
        SeriesPRESS.append(np.sum(SE))
    return SeriesPRESS
    
def Q2(SeriesPRESS, Observation):
    Q2 = []
    for i in range(len(SeriesPRESS)):
        if i == 0:
            Q2.append(1-SeriesPRESS[i]/SeriesPRESS[i])
        else:
            Q2.append(1-SeriesPRESS[i]/SeriesPRESS[i-1])
    
    #### Rule 1: Q2 > limit 
    ####        limit = 0 for observation > 100 
    ####        limit = 0.05 for observation <= 100
    if Observation > 100:
        OptimalPC = [ind for ind, val in enumerate(Q2) if val > 0]
    else:
        OptimalPC = [ind for ind, val in enumerate(Q2) if val > 0.05]
    return OptimalPC
    
def Q2CV(ArrayYpred, Observation):
    import numpy as np
    nrow, ncol = ArrayYpred.shape[0], ArrayYpred.shape[1]
    SE = np.zeros((nrow,ncol-1))
    for i in range(1,ncol):
        SE[:,i-1] = (ArrayYpred[:,i] - ArrayYpred[:,0])**2
    
    Q2 = np.zeros((nrow,ncol-1))
    for ii in range(ncol-1):
        if ii == 0:
            Q2[:,ii] = 1-SE[:,ii]/SE[:,ii]
        else:
            Q2[:,ii] = 1-SE[:,ii]/SE[:,ii-1]
    
    Q2Max = np.max(Q2,axis=0)
    if Observation > 100:
        OptimalPC = [ind for ind, val in enumerate(Q2Max) if val > 0]
    else:
        OptimalPC = [ind for ind, val in enumerate(Q2Max) if val > 0.05]
    return OptimalPC
    
def Decision(r,Q2, Q2CV):
    import numpy as np
    from operator import itemgetter
    ArrayDecision = np.zeros((len(r),3))
    
    ArrayDecision[:,0] = r
    
    for i in Q2:
        ArrayDecision[i,1] = 1
        
    for j in Q2CV:
        ArrayDecision[j,2] = 1
    
    A = sorted(ArrayDecision, key=itemgetter(0))
    for k in range(len(A)):
        if A[-1][1] == 1 or A[-1][2] == 1:
            Q2 = A[-1][0]
            continue
        else:
            A.pop(-1)
    OptimalPC = [ind for ind,val in enumerate(ArrayDecision[:,0]) if val==Q2]
    if OptimalPC == []:
        OpPC = 1
    else:
        OpPC = OptimalPC[0]+1
    return Q2, OpPC
    
def RMSE_Array(ArrayYpred, OptimalPC):
    import numpy as np
    Ypred = ArrayYpred[:,OptimalPC]
    Ytrue = ArrayYpred[:,0]
    SE = (Ytrue-Ypred)**2
    return np.sqrt(np.mean(SE))
    
def RMSE(Ytrue, Ypred):
    import numpy as np
    SE = (np.array(Ytrue)-np.array(Ypred))**2
    return np.sqrt(np.mean(SE))  
    
def ArrayPerformance_sigle_model(Model,R2,Q2,Q2ext,RMSE_tr,RMSE_CV,RMSE_ext):
    import numpy as np
    Array = np.zeros((13,6))
    Array[int(Model[6:])-1,0] = round(R2,3)
    Array[int(Model[6:])-1,1] = round(Q2,3)
    Array[int(Model[6:])-1,2] = round(Q2ext,3)
    Array[int(Model[6:])-1,3] = round(RMSE_tr,3)
    Array[int(Model[6:])-1,4] = round(RMSE_CV,3)
    Array[int(Model[6:])-1,5] = round(RMSE_ext,3)
    return Array
    
def AnalysisPerformance3D(YkeepAll, SumPer, m_re, user):    
    import numpy as np
    import os
    
    C = []
    for k in range(3):
        ConArray = np.zeros((SumPer.shape[0],SumPer.shape[2]))
        for i in range(SumPer.shape[2]):
            ConArray[:,i] = SumPer[:,k,i]
    
        Conmax = np.max(ConArray,axis=1)
        for j in range(ConArray.shape[0]):
            for jj in range(ConArray.shape[1]):
                if ConArray[j,jj] == Conmax[j]:
                    ConArray[j,jj] = 1
                else:
                    ConArray[j,jj] = 0
    
        A = np.sum(ConArray,axis=0)
        B = [ind for ind,val in enumerate(A) if val == np.max(A)]
        C.extend(B)
    unique, counts = np.unique(np.array(C), return_counts=True)
    D = [ind for ind ,val in enumerate(counts) if val == np.max(counts)]
    if len(D) > 1:
        D = np.unique(D[0])

    Y = YkeepAll[:,:,D[0]]

    H = []
    for p in range(13):
        H.append('YtrueM'+str(p+1))
        H.append('YpredM'+str(p+1))

    hM =  np.reshape(np.array(H),(1,len(H)))
    Ykeep = np.append(hM,Y,axis=0)
    
    ############### Eliminate unwanted data ############################
    MI = range(1,14)
    for MII in user['Model_index']:
        if int(MII) == 0:
            MIval = []
        else:
            MIval = [val for ind,val in enumerate(MI) if val!=int(MII)] 
    for v in MIval:  
        Ykeep[1:,2*v-1] = ''
        Ykeep[1:,2*v-2] = ''
    for MIII in user['Model_index']:
        AA = Ykeep[:,2*int(MIII)-1]
        indminus = [ind for ind,val in enumerate(AA) if val=='-1.0']
        Ykeep[indminus,2*int(MII)-1] = ''
        Ykeep[indminus,2*int(MII)-2] = ''
    ####################################################################
    
    path = user['Root']
    IndicatorName = user['Indicator'] 
    try:
        os.makedirs(path+'/'+IndicatorName+'/parameters')
    except OSError:
        pass
    
    return np.mean(SumPer, axis=2), np.std(SumPer, axis=2), Ykeep
    
def ArrayPerformance_class_single_model(Model, classCV, classtr, classext):
    import numpy as np
    Array = np.zeros((13,9))
    Array[int(Model[6:])-1,0] = round(classtr['acc'],3)
    Array[int(Model[6:])-1,1] = round(classCV['acc'],3)
    Array[int(Model[6:])-1,2] = round(classext['acc'],3)
    Array[int(Model[6:])-1,3] = round(classtr['auc'],3)
    Array[int(Model[6:])-1,4] = round(classCV['auc'],3)
    Array[int(Model[6:])-1,5] = round(classext['auc'],3)
    Array[int(Model[6:])-1,6] = round(classtr['matthew'],3)
    Array[int(Model[6:])-1,7] = round(classCV['matthew'],3)
    Array[int(Model[6:])-1,8] = round(classext['matthew'],3)
    return Array
    
def Performance_class(ArrayY):
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import matthews_corrcoef
    from sklearn.metrics import roc_auc_score
    classper = {}
    classper['auc'] = roc_auc_score(ArrayY[:,0], ArrayY[:,1]) 
    classper['acc'] = accuracy_score(ArrayY[:,0], ArrayY[:,1])
    classper['matthew'] = matthews_corrcoef(ArrayY[:,0], ArrayY[:,1])
    
    return ArrayY, classper