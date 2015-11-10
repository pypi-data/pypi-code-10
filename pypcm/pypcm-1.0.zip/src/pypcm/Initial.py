# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:45:33 2015

@author: user01
"""
def userdefined(Rawfile, Indicator, Ligand_index=[], Protein_index=[], Model_index=[1], Predictor='PLS',
                SpiltCriteria=0.15, CV_numfolds=10, FeatureSelectionMode='No', Iteration=20, NumPermute=100):
    
    """Parameters determined by user
    
    Parameters
    ----------
    Rawfile : str
        The filename of data set to be implemented. 
        
    Indicator : str
        The name indicated for saving and showing results.
        
    Ligand_index : int, optional, default = []
        The ligand descriptors were indexed to be automatic genarated using PYDPI
            []   --> no consturcted      0
             0   --> all descriptors   615
             1   --> constitution       30
             2   --> topology           25
             3   --> connectivity       44
             4   --> E-state           237
             5   --> kappa               7
             6   --> Moreau-Boto        32
             7   --> Moran              32
             8   --> Geary              32
             9   --> charge             25
            10   --> property           6
            11   --> MOE-type          60
        Example: If you need construct ligand Gr.1,2,11 you can type [1,2,11]

        
    Protein_index : int, optional, default = []
        The protein descriptors were indexed to be automatic genarated using PYDPI
            []   --> no consturcted                            0
             0   --> all descriptors                        2049
             1   --> amino acid composition                   20
             2   --> dipeptide composition                   400
             3   --> Tripeptide composition                 8000
             4   --> Moreau-Broto autocorrelation            240
             5   --> Moran autocorrelation                   240
             6   --> Geary autocorrelation                   240
             7   --> composition,transition,distribution  21+21+105
             8   --> conjoint triad features                 343
             9   --> sequence order coupling number           60
            10   --> quasi-sequence order descriptors        100
            11   --> pseudo amino acid composition            50
            
    Model_index : int, optional, default = [1]
        The PCM models were indexed to  be automatic generated 
             0   --> All 13 models to be genarated
             1   --> L
             2   --> P
             3   --> LxP
             4   --> LxL
             5   --> PxP 
             6   --> L, P
             7   --> L, P, LxP
             8   --> L, P, LxL
             9   --> L, P, PxP
             10  --> L, P, LxP, LxL
             11  --> L, P, LxP, PxP
             12  --> L, P, LxL, PxP
             13  --> L, P, LxL, PxP, LxP
             
    Predictor : str, default = PLS
        The predictor partial least squred (PLS), random forest (RF), support vector machine (SVM)
        
    Spiltcriteria : float
    
    CV_numfolds = int, default = 10
        The number of folds for cross-validation processing
        
    FeatureSelectionMode : str, default = No
        The option for either select or ignore selection feature importance
        
    Iteration : int, optional, default = 20
        
    NumPermute : int, optional, default = 100
    
    Returns
    -------
    user : tuple
        
        

    """
    import Descriptors_Extraction as Ex
    user = Ex.UserDefined(Rawfile, Indicator, Ligand_index, Protein_index, Model_index, 
                          Predictor, SpiltCriteria, CV_numfolds, FeatureSelectionMode, 
                          Iteration, NumPermute)
    return user
    
def Run(user):
    import PCM_workflow as pcm
    import Descriptors_Extraction as Ex
    Ex.AnalysisInputfile(user)
    X, Y, H, harray, NumDes = pcm.Model_Selection(user)
    ind_ext = pcm.Index_Train_Ext(X, user)
    Mean, SD, Ykeep = pcm.Prediction(X,Y,ind_ext, user)
    Q2_intercept, Scamb = pcm.Yscrambling(X,Y, user)
    pcm.Combine_array(NumDes, harray, Mean, SD, Ykeep, Q2_intercept, Scamb, user)