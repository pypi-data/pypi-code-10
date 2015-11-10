# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:34:42 2015

@author: Wiwat Owasirikul
"""

def PLS(X,Y,kf,user):
    import numpy as np
    from sklearn.cross_decomposition import PLSRegression
    import PredictivePerformance as PP
    import Optimize_Parameters as OP
    
    if X.shape[1] < 10:
         NumPC = X.shape[1]
    else:
        NumPC = 10
        
    ArrayYpredCV = np.zeros((len(Y),NumPC+1))
    Q = []
        
    for PC in range(1, NumPC+1):
        model = PLSRegression(n_components=PC, scale=False)
        YpCV, Q2, RMSE_CV = OP.IterCV(X,Y,model,kf)
        Q.append(Q2)
        ArrayYpredCV[:,PC] = YpCV[:,1]
    ArrayYpredCV[:,0] = YpCV[:,0]
                 
    SeriesPRESS = PP.PRESS(ArrayYpredCV)
    OPC_Q2 = PP.Q2(SeriesPRESS, X.shape[0])
    OPC_Q2CV = PP.Q2CV(ArrayYpredCV,X.shape[0])
    Q2, OptimalPC = PP.Decision(Q,OPC_Q2,OPC_Q2CV)
    RMSE_CV = PP.RMSE_Array(ArrayYpredCV,OptimalPC)
    estimator = PLSRegression(n_components=OptimalPC, scale=False)
    
    YpredCV = np.zeros((len(Y),2))
    YpredCV[:,0] = ArrayYpredCV[:,0]
    YpredCV[:,1] = ArrayYpredCV[:,OptimalPC]
    return YpredCV, np.round(Q2,3), np.round(RMSE_CV,3), estimator
      
def RF(X,Y,kf,user):
    import Optimize_Parameters as OP
    from sklearn.grid_search import GridSearchCV
    import numpy as np
    
#    ntree = np.array([10])
    ntree = np.array(range(10,100,10))
    param_grid = dict(n_estimators = ntree)
    if user['Datatype'] == 'Regression':
        from sklearn.ensemble.forest import RandomForestRegressor
        grid = GridSearchCV(RandomForestRegressor(), param_grid, cv=kf)
    elif user['Datatype'] == 'Classification 2 classes':
        from sklearn.ensemble.forest import RandomForestClassifier
        estimator = RandomForestClassifier()
        grid = GridSearchCV(RandomForestClassifier(), param_grid, cv=kf)
    grid.fit(X,Y)
    estimator = grid.best_estimator_
    YpredCV, Q2, RMSE_CV = OP.IterCV(X,Y,estimator,kf)
    return YpredCV, Q2, RMSE_CV, estimator
    
def SVM(X,Y,kf,user):
    from sklearn import svm
    from sklearn.grid_search import GridSearchCV
    import numpy as np
    import Optimize_Parameters as OP
    
#    C_range = np.array([1])
#    gamma_range = np.array([0])
    C_range = np.logspace(-20,20,20)
    gamma_range = np.logspace(-20,20,20)
    param_grid = dict(gamma=gamma_range, C=C_range) 
    
    if user['Datatype'] == 'Regression':
        grid = GridSearchCV(svm.SVR(), param_grid=param_grid, cv=kf)
    elif user['Datatype'] == 'Classification 2 classes':
        grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=kf)
    grid.fit(X,Y)
    
    estimator = grid.best_estimator_
    YpredCV, Q2, RMSE_CV = OP.IterCV(X,Y,estimator,kf)
    return YpredCV, Q2, RMSE_CV, estimator
    
def IterCV(X,Y,estimator,kf):
    import PredictivePerformance as PP
    import PCM_workflow as PCM
    import numpy as np
    Ytrue, Ypred = [],[]
    for train,test in kf:
        Xtrain, Ytrain = X[train], Y[train]
        Xtest, Ytest = X[test], Y[test]
        YtrueCV,YpredCV,Q2,RMSE_CV = PCM.Prediction_processing(Xtest,Ytest,estimator.fit(Xtrain,Ytrain))
        Ytrue.extend(YtrueCV), Ypred.extend(YpredCV)
    Q2 = PP.rsquared(Ytrue,Ypred)
    RMSE_CV = PP.RMSE(Ytrue, Ypred)
    
    YpredCV = np.zeros((len(Y),2))
    YpredCV[:,0] = Ytrue
    YpredCV[:,1] = Ypred
    return YpredCV, np.round(Q2,3), np.round(RMSE_CV,3)
    