# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 09:19:41 2014

@author: Wiwat Owasirikul
"""

def VIP(X, Y, H, NumDes, user): 
    import numpy as np
    from sklearn.cross_validation import KFold
    import PCM_workflow as PW
    from Descriptors_Selection import Ranking10
    import Optimize_Parameters as OP
    
    print '############## Descriptors selection are being processed ###############'
    M = list(X.viewkeys())
    
    H_VIP, X_VIP, Y_VIP, HArray = {},{},{},{}
    NumDesVIP = np.zeros((13,6), dtype=int)
    for kk in M:
        XTR, YTR = X[kk], Y
        kf = KFold(len(YTR), 10, shuffle=True, random_state=1)
        HH = H[kk] 
        nrow, ncol = np.shape(XTR)
        
        if user['Predictor'] == 'PLS':
            YpCV,Q2,RMSE_CV,estimator = OP.PLS(XTR,YTR,kf, user)
    
            Ytruetr,Ypredtr,R2,RMSE_tr = PW.Prediction_processing(XTR,YTR,estimator.fit(XTR,YTR)) 
            x_scores = estimator.x_scores_
            x_weighted = estimator.x_weights_
            m, p = nrow, ncol
            m, h = np.shape(x_scores)
            p, h = np.shape(x_weighted)
            X_S, X_W = x_scores, x_weighted

            co=[]
            for i in range(h):
                corr = np.corrcoef(np.squeeze(YTR), X_S[:,i])
                co.append(corr[0][1]**2)
            s = sum(co)
            vip=[]
            for j in range(p):
                d=[]
                for k in range(h):
                    d.append(co[k]*X_W[j,k]**2)
                q=sum(d)
                vip.append(np.sqrt(p*q/s))
    
            idx_keep = [idx for idx, val in enumerate(vip) if val >= 1]
            vvip = np.array(vip)[idx_keep]
            idx_keep = Ranking10(idx_keep,vvip)
            
        elif user['Predictor'] == 'RF':
            YpCV,Q2,RMSE_CV,estimator = OP.RF(XTR,YTR,kf,user)
            vip = estimator.feature_importances_
            idx_keep = range(len(vip))
            idx_keep = Ranking10(idx_keep,vip)
            
        elif user['Predictor'] == 'SVM':
            from sklearn.feature_selection import SelectKBest
            YpCV,Q2,RMSE_CV,estimator = OP.SVM(XTR,YTR,kf,user)

            if user['Datatype'] == 'Regression':
                from sklearn.feature_selection import f_regression
                X_new = SelectKBest(f_regression).fit_transform(XTR,YTR)
            if user['Datatype'] == 'Classification 2 classes':
                from sklearn.feature_selection import f_classif
                X_new = SelectKBest(f_classif).fit_transform(XTR,YTR)
                
            vip = range(XTR.shape[1])
            idx_keep = []
            for i in range(X_new.shape[1]):
                A = X_new[:,i]
                idx_keep.extend([ind for ind,val in enumerate(np.transpose(XTR)) if (val==A).all()])
        
        idxDes = NumDes[int(kk[6:])-1,:]
        L,P,LxP,LxL,PxP = [],[],[],[],[] 
        for idx in idx_keep:
            if idx >= 0 and idx < np.sum(idxDes[0:1]):                 
                L.append(idx)
            elif idx >= np.sum(idxDes[0:1]) and idx < np.sum(idxDes[0:2]):
                P.append(idx)
            elif idx >= np.sum(idxDes[0:2]) and idx < np.sum(idxDes[0:3]):
                LxP.append(idx)
            elif idx >= np.sum(idxDes[0:3]) and idx < np.sum(idxDes[0:4]):
                LxL.append(idx)
            elif idx >= np.sum(idxDes[0:4]) and idx < np.sum(idxDes):
                PxP.append(idx)
        
        NVIP= np.array([len(L),len(P),len(LxP),len(LxL),len(PxP),len(idx_keep)])
        NumDesVIP[int(kk[6:])-1,:] = NumDesVIP[int(kk[6:])-1,:]+NVIP

        hvip = np.array(HH)[idx_keep]
        vvip = np.array(vip)[idx_keep]
        H_VIP[kk] = hvip
        X_VIP[kk] = XTR[:,idx_keep]   
        Y_VIP = YTR
    
        hvip = np.reshape(hvip,(len(hvip),1))
        vvip = np.reshape(vvip, (len(vvip),1))
        
        HArray[kk] = np.append(hvip, vvip, axis=1)
        
    return X_VIP, Y_VIP, H_VIP, HArray, NumDesVIP
    
def Ranking10(index, value):
     ##### Reduction of descriptor into the highest 10 order #########
    mapp = []        
    for p in range(len(value)):
        mapp.append((value[p], index[p]))

    mapp_sort = sorted(mapp)
    mapp_select = mapp_sort[-10:]
        
    idx_keep = []
    for pp in range(len(mapp_select)):
        idx_keep.append(mapp_select[pp][1])
    return idx_keep

def VarinceThreshold(X):
    import numpy as np
    STDEV = np.std(X, axis=0)
    return [idx for idx, val in enumerate(STDEV) if val > 0.1]
    
def Correlation(X, Y):
    from scipy.stats import pearsonr
    nrow, ncol = X.shape
    
    Corr_XY = []
    for i in range(ncol):
        Corr_XY.append(pearsonr(X[:,i],Y)[1])
    
    A = [j[0] for j in sorted(enumerate(Corr_XY), key=lambda x:x[1])]
    
    AA = []
    
    while A != []:
        i_keep = []
        for k in range(len(A)):
            if k == 0:
                i_keep.append(1)
            else:
                p = pearsonr(X[:,A[0]], X[:,A[k]])[1]
                if p <= 0.05:     #highly correlation
                    i_keep.append(0)
                else:
                    i_keep.append(1)
        A = [A[ind]for ind,val in enumerate(i_keep) if val == 1] 
        AA.append(A.pop(0)) 
    return AA
    
def VIP_origin(X, Y, H): 
    from sklearn.cross_decomposition import PLSRegression
    import numpy as np
    from sklearn.cross_validation import KFold
    import PCM_workflow as PW
    
    print '############## VIP is being processed ###############'
    Y = Y.astype(np.float)
    
    Xtrain, Ytrain = X, Y
    kf = KFold(len(Ytrain), 10, indices=True, shuffle=True, random_state=1)
    nrow, ncol = np.shape(Xtrain)
        
    ArrayYpredCV, Q2, RMSE_CV, OptimalPC = PW.CV_Processing(Xtrain,Ytrain,kf)
    
    plsmodel = PLSRegression(n_components=OptimalPC)
    plsmodel.fit(Xtrain,Ytrain)
    x_scores = plsmodel.x_scores_
    x_weighted = plsmodel.x_weights_
    m, p = nrow, ncol
    m, h = np.shape(x_scores)
    p, h = np.shape(x_weighted)
    X_S, X_W = x_scores, x_weighted

    co=[]
    for i in range(h):
        corr = np.corrcoef(np.squeeze(Ytrain), X_S[:,i])
        co.append(corr[0][1]**2)
    s = sum(co)
    vip=[]
    for j in range(p):
        d=[]
        for k in range(h):
            d.append(co[k]*X_W[j,k]**2)
        q=sum(d)
        vip.append(np.sqrt(p*q/s))
    
    idx_keep = [idx for idx, val in enumerate(vip) if vip[idx] >= 1]
    H_VIP = np.squeeze(np.array(H))[idx_keep]
    X_VIP = Xtrain[:,idx_keep]   
    Y_VIP = Ytrain
    return X_VIP, Y_VIP, H_VIP