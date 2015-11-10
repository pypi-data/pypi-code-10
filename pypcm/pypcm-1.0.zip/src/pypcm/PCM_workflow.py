# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 08:57:58 2014

@author: Wiwat Owasirikul
"""   
def Xval_nonPCM(X,h,Y,user):
    import os,pickle
    import numpy as np
    path = user['Root'] 
    IndicatorName = user['Indicator']
    X = X.astype(np.float)
    XX = {}
    XX['X'] = X
    XX['H'] = h
    if user['Datatype'] == 'Regression':
        XX['Y'] = np.delete(Y,0,axis=0).astype(np.float)
    else:
        XX['Y'] = np.delete(Y,0,axis=0)
    try:
        os.makedirs(path+'/'+IndicatorName+'/XVAL')
    except OSError:
        pass
    
            
    Xval_path = path+'/'+IndicatorName+'/XVAL'
            
    if len(os.listdir(Xval_path)) > 0:
        pass
    else:
        out = open(Xval_path+'/X1'+'.pkl','wb')
        pickle.dump(XX, out)
        out.close()
            
        NumDes = np.zeros((13,6),dtype=np.int)
        NumDes[0,0], NumDes[0,-1] = len(h), len(h) 
        out1 = open(Xval_path+'/NumDes.pkl','wb')
        pickle.dump(NumDes, out1)
        out1.close() 
        
def Xval(DL,DP,Y, user):
    import numpy as np
    import ProChem as PCM
    import pickle, os
    
    path = user['Root']
    IndicatorName = user['Indicator']
    
    try:
        os.makedirs(path+'/'+IndicatorName+'/XVAL')
    except OSError:
        pass
    Xval_path = path+'/'+IndicatorName+'/XVAL'
    
    if len(os.listdir(Xval_path)) > 0:
        pass
    else:
        header_protein, protein = DP[0,:], np.delete(DP,0,axis=0).astype(np.float)
        header_ligand, ligand  = DL[0,:], np.delete(DL,0,axis=0).astype(np.float)
        Li_Li, header_Li_Li = PCM.Combine_Ligand_Ligand(ligand, list(header_ligand))
        Pro_Pro, header_Pro_Pro = PCM.Combine_Protein_Protein(protein, list(header_protein))
        Li_Pro, header_Li_Pro = PCM.Combine_Ligand_Protein(ligand, list(header_ligand), protein, list(header_protein))
   
        ## mean centering and scaling 
        ligand = PCM.Normalized(ligand) 
        protein = PCM.Normalized(protein)
        Li_Li = PCM.Normalized(Li_Li)
        Li_Pro = PCM.Normalized(Li_Pro) 
        Pro_Pro = PCM.Normalized(Pro_Pro)
        
        NumDes = np.zeros((13,5),dtype=np.int)
        
        XX = {}
        ######################## Build 13 PCM models ###########################    
        for model_iter in range(1,14):
            if model_iter == 1:   #model 1: Ligand only
                print 'Model 1: L'
                X, header = ligand, header_ligand 
                NumDes[model_iter-1,model_iter-1] = len(header_ligand)
            elif model_iter == 2:  #model 2: Protein only
                print 'Model 2: P'
                X, header = protein, header_protein
                NumDes[model_iter-1,model_iter-1] = len(header_protein)
            elif model_iter == 3:  #model 3: LxP
                print 'Model 3: LxP'
                X, header = Li_Pro, header_Li_Pro
                NumDes[model_iter-1,model_iter-1] = len(header_Li_Pro)
            elif model_iter == 4:  #model 4: LxL
                print 'Model 4: LxL'
                X, header = Li_Li,  header_Li_Li
                NumDes[model_iter-1,model_iter-1] = len(header_Li_Li)
            elif model_iter == 5:  #model 5: PxP
                print 'Model 5: PxP'
                X, header = Pro_Pro, header_Pro_Pro
                NumDes[model_iter-1,model_iter-1] = len(header_Pro_Pro)
            elif model_iter == 6:      #model 6: L, P
                print 'Model 6: L, P'
                X,header = PCM.Inputs_2(ligand, header_ligand,
                                        protein, header_protein)
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
            elif model_iter == 7:   #model 7: L, P, LxP 
                print 'Model 7: L, P, LxP'
                X, header = PCM.Inputs_3(ligand, header_ligand,                                            
                                         protein, header_protein,
                                         Li_Pro, header_Li_Pro)            
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
                NumDes[model_iter-1,2] = len(header_Li_Pro)
    
            elif model_iter == 8:   #model 8: L, P, LxL
                print 'Model 8: L, P, LxL'
                X, header = PCM.Inputs_3(ligand, header_ligand,
                                         protein, header_protein,
                                         Li_Li, header_Li_Li)
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
                NumDes[model_iter-1,3] = len(header_Li_Li)
        
            elif model_iter == 9:   #model 9: L, P, PxP
                print 'Model 9: L, P, PxP'
                X, header = PCM.Inputs_3(ligand, header_ligand,
                                         protein, header_protein,
                                         Pro_Pro, header_Pro_Pro)
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
                NumDes[model_iter-1,4] = len(header_Pro_Pro)
        
            elif model_iter == 10:   #model 10: L, P, LxP, LxL
                print 'Model 10: L, P, LxP, LxL'
                X, header = PCM.Inputs_4(ligand, header_ligand,
                                         protein, header_protein,
                                         Li_Pro, header_Li_Pro,
                                         Li_Li, header_Li_Li) 
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
                NumDes[model_iter-1,2] = len(header_Li_Pro)
                NumDes[model_iter-1,3] = len(header_Li_Li)
                                       
            elif model_iter == 11:   #model 11: L, P, LxP, PxP
                print 'Model 11: L, P, LxP, PxP'
                X, header = PCM.Inputs_4(ligand, header_ligand,
                                         protein, header_protein,
                                         Li_Pro, header_Li_Pro,
                                         Pro_Pro, header_Pro_Pro)
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
                NumDes[model_iter-1,2] = len(header_Li_Pro)
                NumDes[model_iter-1,4] = len(header_Pro_Pro)
                                                               
            elif model_iter == 12:   #model 7: L, P, LxL, PxP
                print 'Model 12: L, P, LxL, PxP'
                X, header = PCM.Inputs_4(ligand, header_ligand,
                                         protein, header_protein,
                                         Li_Li, header_Li_Li,
                                         Pro_Pro, header_Pro_Pro)
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
                NumDes[model_iter-1,3] = len(header_Li_Li)
                NumDes[model_iter-1,4] = len(header_Pro_Pro)
                                         
            elif model_iter == 13:   #model 8: L, P, LxL, PxP, LxP
                print 'Model 13: L, P, LxL, PxP, LxP'
                X, header = PCM.Inputs_5(ligand, header_ligand,
                                         protein, header_protein,
                                         Li_Li, header_Li_Li,
                                         Pro_Pro, header_Pro_Pro,
                                         Li_Pro, header_Li_Pro)
                NumDes[model_iter-1,0] = len(header_ligand)
                NumDes[model_iter-1,1] = len(header_protein)
                NumDes[model_iter-1,2] = len(header_Li_Pro)
                NumDes[model_iter-1,3] = len(header_Li_Li)
                NumDes[model_iter-1,4] = len(header_Pro_Pro)
            XX['X'] = X
            XX['H'] = header
            XX['Y'] = np.delete(Y,0,axis=0).astype(np.float)
        
            out = open(Xval_path+'/X'+str(model_iter)+'.pkl','wb')
            pickle.dump(XX, out)
            out.close()
        
        sumNumDes = np.reshape(np.sum(NumDes,axis=1), (13,1))
        NumDes = np.append(NumDes, sumNumDes ,axis=1)
        out1 = open(Xval_path+'/NumDes.pkl','wb')
        pickle.dump(NumDes, out1)
        out1.close()
            
def Model_Selection(user):
    index = user['Model_index']
    Descriptors_Selection = user['SelectionMode']
    IndicatorName = user['Indicator']
    path = user['Root']
    
    import pickle
    import numpy as np
    
    Xval_path = path+'/'+IndicatorName+'/XVAL'
    index = [int(i) for i in index]
    NumDes = pickle.load(open(Xval_path+'/NumDes.pkl','rb'))
    indexrunning = range(1,14)
    if index != [0]:
        indexrunning = list(set(indexrunning)-set(index))
        for ii in indexrunning:
            NumDes[ii-1,:] = 0
    else:
        index = range(1,14)

    Var_X, Var_header = {},{}   
    for i in index:
        D = pickle.load(open(Xval_path+'/'+'X'+str(i)+'.pkl','rb'))
        Var_X['Model_'+str(i)] = D['X']
        Var_header['Model_'+str(i)] = D['H']
        Var_Y = D['Y']  
    
    ######################## Build number descriptors array #################
    h_list = ['L','P','LxP','LxL','PxP','Total']
    h_num =  np.reshape(np.array(h_list),(1,6))
    #########################################################################    
    if Descriptors_Selection == 'No':
        NumDes = np.append(h_num,NumDes,axis=0)
        harray = Var_header
    elif Descriptors_Selection == 'Yes':
        from Descriptors_Selection import VIP
        Var_X, Var_Y, Var_header, harray, NumDes = VIP(Var_X, Var_Y, Var_header, NumDes, user)
        NumDes = np.append(h_num,NumDes,axis=0)
        
    return  Var_X, Var_Y, Var_header, harray, NumDes 
        
def Index_Train_Ext(X, user):
    Criteria = user['Splitcriteria']
    Iter = user['Iteration']
    import numpy as np
    from sklearn import cross_validation 
    M = list(X.viewkeys())
    
    numcol = []
    for j in M:
        numcol.append(X[j].shape[1])
    idx_M = [ind for ind,val in enumerate(numcol) if val == np.min(np.array(numcol))]
    
    X = X[M[idx_M[0]]]
    k = int(np.round(1/Criteria))
    ind_ext_out = []
    for i in range(Iter):
        kf = cross_validation.KFold(X.shape[0],n_folds=k,shuffle=True,random_state=None)
        ind_ext = []        
        for tr,te in kf:
            ind_ext.append(te)
        ind_ext_out.append(ind_ext)
    return ind_ext_out
    
def Prediction(XM, Y, ind_ext, user):
    Criteria = user['Splitcriteria']
    Iter = user['Iteration']
    Predictor = user['Predictor']
    import numpy as np
    import PredictivePerformance as PP
    import PCM_workflow as PW 
    from sklearn import cross_validation 
    
    print '############## Prediction is being processed ###############'
    M = list(XM.viewkeys())
    m_re = []
    for m in M:
        m_re.append(int(m[6:]))
    m_re = sorted(m_re)
    m_re = ['Model_'+str(j) for j in m_re]
    
    YkeepALL = np.zeros((2*len(Y),26,Iter)) 
    
    if user['Datatype'] == 'Regression':
        PerALL = np.zeros((13,6,Iter))
    elif user['Datatype'] == 'Classification 2 classes':
        PerALL = np.zeros((13,9,Iter))

        
    K = int(np.round(1/Criteria))
        
    for k in range(Iter):   ## Kernald-stone algorithm
        print 'Iteration: %i' %(k+1)
        kfext = cross_validation.KFold(len(Y),n_folds=K,shuffle=True,random_state=None)
        
        if user['Datatype'] == 'Regression':
            Performance = np.zeros((13,6))
        elif user['Datatype'] == 'Classification 2 classes':
            Performance = np.zeros((13,9))

        Ykeep = np.zeros((2*len(Y),26))

        for ind_M in m_re:
            print ind_M +' is being processed'   ## Model selection
            X = XM[ind_M].astype(np.float) 
            Y = np.array(Y).astype(np.float)
            ##Inner cross-validation
            mR2, mQ2, mP2, mRMSE_tr, mRMSE_CV, mRMSE_ext, mYptr, mYpCV, mYpext = PW.multiprocess_InnerCV(X,Y,kfext,user)

            iMaxQ2 = [ind for ind, val in enumerate(mQ2) if val == np.max(mQ2)]
            maxYtr = mYptr[iMaxQ2[0]]
            maxYCV = mYpCV[iMaxQ2[0]]
            maxYext = mYpext[iMaxQ2[0]]
            
            if user['Datatype'] == 'Classification 2 classes':
                if Predictor == 'PLS':
                    maxYCV, classCV = PW.Classify_using_threholding2(maxYCV)
                    maxYtr, classtr = PW.Classify_using_threholding2(maxYtr)
                    maxYext,classext = PW.Classify_using_threholding2(maxYext)
                else:
                    maxYCV, classCV = PP.Performance_class(maxYCV)
                    maxYtr, classtr = PP.Performance_class(maxYtr)
                    maxYext, classext = PP.Performance_class(maxYext)
            
            A, B, C = len(maxYtr), len(maxYCV), len(maxYext)
            
            Ykeep[:A,2*(int(ind_M[6:]))-2] = maxYtr[:,0]
            Ykeep[:A,2*(int(ind_M[6:]))-1] = maxYtr[:,1]

            Ykeep[A,2*(int(ind_M[6:]))-2] = int(-1)
            Ykeep[A,2*(int(ind_M[6:]))-1] = int(-1)
            
            Ykeep[A+1:A+B+1,2*(int(ind_M[6:]))-2] = maxYCV[:,0]
            Ykeep[A+1:A+B+1,2*(int(ind_M[6:]))-1] = maxYCV[:,1]
            
            Ykeep[A+B+1,2*(int(ind_M[6:]))-2] = int(-1)
            Ykeep[A+B+1,2*(int(ind_M[6:]))-1] = int(-1)
            
            Ykeep[A+B+2:A+B+C+2, 2*(int(ind_M[6:]))-2] = maxYext[:,0]
            Ykeep[A+B+2:A+B+C+2, 2*(int(ind_M[6:]))-1] = maxYext[:,1]
            
            Ykeep[A+B+C+2:, 2*(int(ind_M[6:]))-2] = int(-1)
            Ykeep[A+B+C+2:, 2*(int(ind_M[6:]))-1] = int(-1)
            
            r2 = np.round(np.mean(mR2),3)
            q2 = np.round(np.mean(mQ2),3)
            p2 = np.round(np.mean(mP2),3)
            rmse_tr = np.round(np.mean(mRMSE_tr),3)
            rmse_cv = np.round(np.mean(mRMSE_CV),3)
            rmse_ext = np.round(np.mean(mRMSE_ext),3)
            
            if user['Datatype'] == 'Regression':
                Performance = Performance + PP.ArrayPerformance_sigle_model(ind_M, r2,q2,p2,rmse_tr,rmse_cv,rmse_ext)
            elif user['Datatype'] == 'Classification 2 classes':
                Performance = Performance + PP.ArrayPerformance_class_single_model(ind_M, classCV, classtr, classext)

        YkeepALL[:,:,k] = Ykeep
        PerALL[:,:,k] = Performance
        
    return PP.AnalysisPerformance3D(YkeepALL, PerALL, m_re, user)
    
def InnerCV(X,Y,TR,ext, user):
    CV_numfolds = user['CV_numfolds']
    Predictor = user['Predictor']
    import Method_SamplingData as MS
    import Optimize_Parameters as OP
    import PCM_workflow as PW 
    import numpy as np

    XTR, YTR = X[TR], Y[TR]
    Xext,Yext = X[ext], Y[ext]
    kf = MS.CV_determination(YTR,CV_numfolds)
                
    #######################  CV processing #######################
    if Predictor == 'PLS':
        YpCV,Q2,RMSE_CV,estimator = OP.PLS(XTR,YTR,kf,user)
            
    elif Predictor == 'RF':
        YpCV,Q2,RMSE_CV,estimator = OP.RF(XTR,YTR,kf,user)
                    
    elif Predictor == 'SVM':
        YpCV,Q2,RMSE_CV,estimator = OP.SVM(XTR,YTR,kf, user)
        ##############################################################
    
    Ytruetr,Ypredtr,R2,RMSE_tr = PW.Prediction_processing(XTR,YTR,estimator.fit(XTR,YTR)) 
    Ytrueext,Ypredext,P2,RMSE_ext = PW.Prediction_processing(Xext,Yext,estimator.fit(XTR,YTR)) 
                
    Yptr = np.append(np.reshape(Ytruetr,(len(Ytruetr),1)),np.reshape(Ypredtr,(len(Ypredtr),1)),axis=1)
    Ypext = np.append(np.reshape(Ytrueext,(len(Ytrueext),1)),np.reshape(Ypredext,(len(Ypredext),1)),axis=1)
        
    return Q2,R2,P2,RMSE_tr,RMSE_CV,RMSE_ext,Yptr,YpCV,Ypext
        
def multiprocess_InnerCV(X,Y,kfext,user):
    import numpy as np
    X = X.astype(np.float)
    import multiprocessing as mp
    mp.freeze_support()
    p = mp.Pool(processes=mp.cpu_count())
    results = [p.apply_async(InnerCV,args=(X,Y,TR,ext,user)) for TR,ext in kfext]
    result = [pp.get() for pp in results]
    
    mR2, mQ2, mP2, mRMSE_tr, mRMSE_CV, mRMSE_ext = [],[],[],[],[],[]
    mYptr, mYpCV, mYpext = [],[],[]
    for i in range(len(result)):
        mR2.append(result[i][0]), mQ2.append(result[i][1]), mP2.append(result[i][2])
        mRMSE_tr.append(result[i][3]), mRMSE_CV.append(result[i][4]), mRMSE_ext.append(result[i][5])
        mYptr.append(result[i][6]), mYpCV.append(result[i][7]), mYpext.append(result[i][8])
    return mR2, mQ2, mP2, mRMSE_tr, mRMSE_CV, mRMSE_ext, mYptr, mYpCV, mYpext 

def Yscrambling(XM,Y,user):
    if user['Datatype'] == 'Regression':
        numfolds = user['CV_numfolds']
        NumPermute = user['NumPermute']

        import numpy as np
        from scipy import stats
        import Method_SamplingData as MS
    
        print '############## Yscambling is being processed ###############'
        YY = []
        while len(YY) != NumPermute:
            Ypermute = np.random.permutation(Y)
            if Ypermute.all == Y.all:
                pass
            else:
                YY.append(Ypermute)
        YYY = []
        for indPer in range(len(YY)+1):
            if indPer == 0:
                YYY.append(Y)
            else:
                YYY.append(YY[indPer-1])

        M = list(XM.viewkeys())  
        m_re = []
        for m in M:
            m_re.append(int(m[6:]))
        m_re = sorted(m_re)
        m_re = ['Model_'+str(j) for j in m_re]
        Q2_intercept = np.zeros((13,2))  
        RQ_array = np.zeros((NumPermute+1,26))    
        for ind_M in m_re:
            print ind_M +'....'
            Xtr = XM[ind_M]
            kf = MS.CV_determination(Y,numfolds)
            RR2,QQ2 = multiprocess_Yscamp(Xtr,YYY,kf, user)
            slope, intercept, r_value, p_value, std_err = stats.linregress(RR2,QQ2)
            
            iR2 = -float(intercept)/float(slope)
            Q2_intercept[int(ind_M[6:])-1,0] = round(iR2,3)
            Q2_intercept[int(ind_M[6:])-1,1] = round(intercept,3) 

            RQ_array[:,(int(ind_M[6:])*2)-2] = RR2
            RQ_array[:,(int(ind_M[6:])*2)-1] = QQ2
    
        Mlist = []
        for i in range(26):
            if np.mod(i,2) == 0:
                Mlist.append('R2_M'+str(np.round(i/2)+1))
            else:
                Mlist.append('Q2_M'+str(np.round(i/2)+1))
    
        hM =  np.reshape(np.array(Mlist),(1,26))
        hM = np.append(hM,RQ_array,axis=0)
        
        ############### Eliminate unwanted data ############################
        MI = range(1,14)
        for MII in user['Model_index']:
            if int(MII) == 0:
                MIval = []
            else:
                MIval = [val for ind,val in enumerate(MI) if val!=int(MII)]
        for v in MIval:  
            hM[1:,2*v-1] = ''
            hM[1:,2*v-2] = ''
        ####################################################################

        return Q2_intercept, hM
    else:
        return [], []
        
def Yscamp_mp(Xtr,Ytr,kf,user):
    Predictor = user['Predictor']
    import Optimize_Parameters as OP
    import PCM_workflow as PW
    ##### Cross-validation processing ################# 
    if Predictor == 'PLS':
        YpCV,Q2,RMSE_CV,estimator = OP.PLS(Xtr,Ytr,kf,user)
                    
    elif Predictor == 'RF':
        YpCV,Q2,RMSE_CV,estimator = OP.RF(Xtr,Ytr,kf,user)
                    
    elif Predictor == 'SVM':
        YpCV,Q2,RMSE_CV,estimator = OP.SVM(Xtr,Ytr,kf, user)
    ###################################################
    Ytruetr,Ypredtr,R2,RMSE_tr = PW.Prediction_processing(Xtr,Ytr,estimator.fit(Xtr,Ytr)) 
    return R2, Q2

def multiprocess_Yscamp(X,YY,kf, user):
    import multiprocessing as mp
    mp.freeze_support()
    pool = mp.Pool(processes=mp.cpu_count())
    results = [pool.apply_async(Yscamp_mp,args=(X,Y,kf,user)) for Y in YY]
    result=[]    
    for p in results:
        result.append(p.get())
        print "%s: %d%%" % ("Processing", (float(len(result))/len(YY))*100)

    RR2,QQ2 =[],[]
    for i in range(len(result)):
        RR2.append(result[i][0]), QQ2.append(result[i][1]),
    return RR2, QQ2
    
def Prediction_processing(X,Y,estimator):
    import numpy as np
    import PredictivePerformance as PP
    Ypred = np.squeeze(estimator.predict(X))
    Ytrue = np.squeeze(Y)
    R2 = PP.rsquared(Y,Ypred)
    RMSE = PP.RMSE(Y, Ypred)
    return Ytrue, Ypred,np.round(R2,3),np.round(RMSE,3)
    
def Classify_using_threholding2(ArrayY):
    import numpy as np
    from sklearn.metrics import matthews_corrcoef
    import PredictivePerformance as PP
    
    Ypred = ArrayY[:,1]
    YC = np.zeros((len(Ypred),1))
    numYpred = np.unique(np.sort(Ypred))
    start = np.round(len(numYpred)*0.1,0)
    end = np.round(len(numYpred)*0.9,0)

    results = []
    for i in range(int(start), int(end)):
        YpC = np.zeros((len(Ypred),1))
        for j in range(len(Ypred)):
            if Ypred[j] >= numYpred[i]:
                YpC[j] = 1   
    
        results.append(matthews_corrcoef(ArrayY[:,0], YpC))
        YC = np.append(YC,YpC,axis=1)

    inx = [ind for ind,val in enumerate(results) if val == max(results)]
    ArrayY[:,1] = YC[:,inx[0]+1]
    
    return PP.Performance_class(ArrayY)
    
def Combine_array(NumDes,h, Mean,SD,Ykeep,Q2permute,Scamb,user):
    IndicatorName = user['Indicator']
    import numpy as np
    import xlsxwriter
    
    A = user['Date Started']
    A = A.replace(":",";")
    path = user['Root']
    fileout = path+'/'+IndicatorName+'/'+'Performance'+A+'.xlsx'  
    
    workbook = xlsxwriter.Workbook(fileout)
    
    #################### Write USERDEFINED Worksheet ###############
    worksheet = workbook.add_worksheet('UserDefined')
    Listuser = list(user.viewkeys())
    
    Valueuser = list(user.viewvalues())
    Valueuser = [str(k) for k in Valueuser] 
    
    l,v = Listuser, Valueuser
    print l
    L = [l[2],l[3],l[11],l[9],l[5],l[12],l[4],l[0],l[6],l[1],l[7],l[10],l[8]]
    V = [v[2],v[3],v[11],v[9],v[5],v[12],v[4],v[0],v[6],v[1],v[7],v[10],v[8]]

    for ii in range(len(Listuser)):
        worksheet.write(ii,0,L[ii])
        worksheet.write(ii,1,V[ii])
         
    ################### Write Performance Worksheet ################
    worksheet = workbook.add_worksheet('SummarizedResults')
    n,m = np.shape(Mean)[0], np.shape(Mean)[1] 
    array_mean_SD = np.zeros((n,m)).astype(np.str)
    for i in range(n):
        for j in range(m):
            array_mean_SD[i,j] = str(np.round(Mean[i,j],3))+' +- '+str(np.round(SD[i,j],3))
    
    if user['Datatype'] == 'Regression':
        array_mean_SD_Q = np.append(array_mean_SD,Q2permute,axis=1)   
        Mlist = ['R^2','Q^2','P^2','RMSE_tr','RMSE_CV','RMSE_ext', 'iR^2','iQ^2']
    elif user['Datatype'] == 'Classification 2 classes':
        Mlist = ['accTr','accCv','accExt','aucTr','aucCv','aucExt','mattTr','mattCv','mattExt']
        array_mean_SD_Q  = array_mean_SD
    hM =  np.reshape(np.array(Mlist),(1,len(Mlist)))
    hM = np.append(hM,array_mean_SD_Q,axis=0)
    
    array = np.append(NumDes,hM,axis=1)
    
    for jj in range(np.shape(array)[0]):
        for kk in range(np.shape(array)[1]):
            worksheet.write(jj,kk,array[jj,kk])
    workbook.close()
    
    ####################################################################
    fileout1 = path+'/'+IndicatorName+'/parameters/'+A+'.xlsx'
    workbook1 = xlsxwriter.Workbook(fileout1)
    
    worksheet = workbook1.add_worksheet('Y')
    for jj in range(np.shape(Ykeep)[0]):
        for kk in range(np.shape(Ykeep)[1]):
            worksheet.write(jj,kk,Ykeep[jj,kk])
            
    worksheet = workbook1.add_worksheet('Yscrambling')
    for jj in range(np.shape(Scamb)[0]):
        for kk in range(np.shape(Scamb)[1]):
            worksheet.write(jj,kk,Scamb[jj,kk])
    
    index = user['Model_index'] 
    if index == ['0']:
        index = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
    if user['SelectionMode'] == 'None':
        for jjjj in index:
            worksheet = workbook1.add_worksheet('Model_'+jjjj)
            for jj in range(len(h['Model_'+jjjj])):
                worksheet.write(jj,0,h['Model_'+jjjj][jj])
    elif user['SelectionMode'] == 'VIP':    
        for jjjj in index:
            worksheet = workbook1.add_worksheet('Model_'+jjjj)
            hh = h['Model_'+jjjj]
            for jj in range(np.shape(hh)[0]):
                for kk in range(np.shape(hh)[1]):
                    worksheet.write(jj,kk,hh[jj,kk])
    
    workbook.close()
    print 'Complete processing --> Investigate the results'