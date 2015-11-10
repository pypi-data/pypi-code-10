# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 10:08:00 2014

@author: Wiwat Owasirikul
"""
def UserDefined(Rawfile, Indicator,Ligand_index,Protein_index, Model_index,Predictor,SplitCriteria,
               CV_numfolds,FeatureSelectionMode, Iteration, NumPermute):
    user = {}
    sep = Rawfile.rpartition('\\')
    user['Root'] = sep[0]
    user['Rawfile'] = Rawfile
    user['Indicator'] = Indicator
    user['Ligand_index'] = Ligand_index
    user['Protein_index'] = Protein_index
    user['Model_index'] = Model_index
    user['Predictor'] = Predictor
    user['Splitcriteria'] = SplitCriteria
    user['CV_numfolds'] = CV_numfolds
    user['SelectionMode'] = FeatureSelectionMode
    user['Iteration'] = Iteration
    user['NumPermute'] = NumPermute
    
    from time import gmtime, strftime
    user['Date Started'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return user
    
def AnalysisInputfile(user):
    Root = user['Root']
    Rawfile = user['Rawfile']
    Indicator = user['Indicator']
    Proteingroup = user['Protein_index']  
    Ligandgroup = user['Ligand_index'] 
    
    import csv, os
    import numpy as np
    import PCM_workflow as pcm
#    fileName = Root+'/'+ Indicator+'.csv'
    
    with open(Rawfile,'rb') as csvfile:
        dialect = csv.Sniffer().has_header(csvfile.read())
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        h = next(reader)
        data = []
        for row in reader:
            data.append(row)
        data_array = np.array(data)

    Yname = h.pop(-1)
    Y_array = np.append(np.reshape(np.array(Yname),(1,1)),data_array[:,-1])
    
    Yunique = np.unique(data_array[:,-1])
    
    if len(Yunique) > 5:  #regression
        user['Datatype'] = 'Regression'
    else: 
        user['Datatype'] = 'Classification ' + str(len(Yunique)) + ' classes'
    
    if Ligandgroup == [''] and Proteingroup == ['']:  ### NO building descriptor ####
        print 'All Descriptors were prepared by user'
        ise = [ind for ind,val in enumerate(h) if val == '']
        
        if ise != []: #### Checking PCM model
            hi = np.reshape(np.array(h), (1,len(h)))
            hf = np.reshape(np.array(Yname), (1,1))
            h = np.append(hi,hf, axis=1)
        
            data_array = np.append(h,data_array,axis=0)
            Array_ligand = data_array[:,:ise[0]]
            Array_Pro = data_array[:,ise[0]+1:-1]
            
            pcm.Xval(Array_ligand,Array_Pro,Y_array, user)
        else:   #### Checking non-PCM model
            X = data_array[:,:-1]
            pcm.Xval_nonPCM(X,h,Y_array,user)
    else:   ####  Process of Buidiling descriptor  #############
        try:
            os.makedirs(Root+'/'+Indicator)
        except OSError:
            pass
        
        Des_path = Root+'/'+Indicator
    
        if [ind for ind,val in enumerate(os.listdir(Des_path)) if val == '_complete.csv'] != []:
            pass
        else:
            psmiles = [ind for ind, val in enumerate(h) if val[:5] == 'Smiles' or val[:5] == 'smiles' or val=='MolSmiles']
            psequence = [ind for ind, val in enumerate(h) if val[:8] == 'Sequence' or val[:8] == 'sequence']
        
            if len(psmiles) == 1 and len(psequence) == 0:
                print 'Ligand descriptors will be generated'
                import Descriptors_Extraction as DE
                data = data_array[:,psmiles[0]]
                Array_ligand = DE.Ligand_gen(data, Ligandgroup)
                px = [ind for ind,val in enumerate(h) if ind!=psmiles[0]]
                hx = np.array(h)[px]
                Array_Pro = np.append(np.reshape(hx,(1,len(hx))),data_array[:,px],axis=0)
        
            elif len(psmiles) == 0 and len(psequence) == 1:
                print 'Protein descriptors will be generated'
                import Descriptors_Extraction as DE
                data = data_array[:,psequence[0]]
                Array_Pro = DE.Protein_gen(data,Proteingroup)
                px = [ind for ind,val in enumerate(h) if ind!=psequence[0]]
                hx = np.array(h)[px]
                Array_ligand = np.append(np.reshape(hx,(1,len(hx))),data_array[:,px],axis=0)
        
            elif len(psmiles) == 1 and len(psequence) == 1:
                print 'Ligand & Protein descriptors will be generated'
                import Descriptors_Extraction as DE
                data1 = data_array[:,psmiles[0]]
                data2 = data_array[:,psequence[0]]
                Array_ligand = DE.Ligand_gen(data1,Ligandgroup)
                Array_Pro = DE.Ligand_gen(data2,Proteingroup)
        
            elif len(psmiles) == 2 and len(psequence) == 0:
                print 'Two different Ligand descriptors will be generated'
                import Descriptors_Extraction as DE
                data1 = data_array[:,psmiles[0]]
                data2 = data_array[:,psmiles[1]]
                Array_ligand = DE.Ligand_gen(data1,Ligandgroup)
                Array_Pro = DE.Ligand_gen(data2,Proteingroup)
        
            elif len(psmiles) == 0 and len(psequence) == 2:
                print 'Two different Protein descriptors will be generated'
                import Descriptors_Extraction as DE
                data1 = data_array[:,psequence[0]]
                data2 = data_array[:,psequence[1]]
                Array_ligand = DE.Protein_gen(data1,Ligandgroup)
                Array_Pro = DE.Protein_gen(data2,Proteingroup)
                
            import PCM_workflow as pcm
            pcm.Xval(Array_ligand,Array_Pro,Y_array, user)
        
################# Comnbine All array for saving ##############
            emp = np.array([None for i in range(Array_Pro.shape[0])])
            emp = np.reshape(emp, (emp.shape[0],1))
            
            Array = np.append(Array_ligand, emp, axis=1)
            Array = np.append(Array, Array_Pro, axis=1)
            Array = np.append(Array, np.reshape(Y_array,(len(Y_array),1)), axis=1)
        
            with open(Des_path+'/_complete.csv', 'wb') as csvfile:
                spam = csv.writer(csvfile,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL )
                for k in range(len(Array)):
                    spam.writerow(Array[k])
   
def Ligand_gen(data, Ligandgroup):
    import numpy as np
    from pydpi.pydrug import PyDrug
    drug=PyDrug()

    HL_list, D_list = [], []
        
    for i in range(len(data)):
        drug.ReadMolFromSmile(data[i])
        keys, values = [],[]
        
        for j in Ligandgroup:
            if j == 0:    #all descriptors   615
                res = drug.GetAllDescriptor()
            elif j == 1:    # constitution   30
                res = drug.GetConstitution()
            elif j == 2:    # topology       25
                res = drug.GetTopology()
            elif j == 3:    #connectivity    44
                res = drug.GetConnectivity()
            elif j == 4:    #E-state         237
                res = drug.GetKappa()
            elif j == 5:    #kappa            7
                res = drug.GetEstate()
            elif j == 6:    #Moreau-Boto      32
                res = drug.GetMoreauBroto()
            elif j == 7:    #Moran            32
                res = drug.GetMoran()
            elif j == 8:   #Geary            32
                res = drug.GetGeary()
            elif j == 9:   #charge           25
                res = drug.GetCharge()
            elif j == 10:   #property          6
                res = drug.GetMolProperty()
            elif j == 11:   #MOE-type          60
                res = drug.GetMOE()
            
            keys.extend(res.viewkeys())
            values.extend(res.viewvalues())
        
        if i == 0:
            HL_list = keys
            D_list.append(values)
        else:
            D_list.append(values)

    D_ligand = np.zeros((len(data),len(HL_list)), dtype=float)
    for k in range(len(data)):
        D_ligand[k,:] = D_list[k]   
    
    #Variance threshold       std > 0.01  
    import Descriptors_Selection as DesSe
    ind_var = DesSe.VarinceThreshold(D_ligand)
    D_ligand = D_ligand[:,ind_var]
    HL_list = np.array(HL_list)[ind_var]
        
#    #Intra pearson's correlation           p-value > 0.05
#    ind_corr = DesSe.Correlation(D_ligand, Y.astype(np.float))
#    D_ligand = D_ligand[:,ind_corr]
#    HL_list = np.array(HL_list)[ind_corr]
        
    H_ligand = np.reshape(HL_list,(1,len(HL_list)))
    Array_ligand = np.append(H_ligand, D_ligand, axis=0) 
    return Array_ligand

def Protein_gen(data, Proteingroup):
    import numpy as np
    from pydpi.pypro import PyPro
    protein = PyPro() 
    
    HP_list, D_list = [], []     
    for ii in range(len(data)):
        p = data[ii]
        protein.ReadProteinSequence(p)
        keys, values = [],[]
        for jj in Proteingroup:
            if jj == 0:    #All descriptors          2049
                res = protein.GetALL()
            elif jj == 1:    #amino acid composition   20
                res = protein.GetAAComp()
            elif jj == 2:    #dipeptide composition    400
                res = protein.GetDPComp()
            elif jj == 3:    #Tripeptide composition   8000
                res = protein.GetTPComp()
            elif jj == 4:    #Moreau-Broto autocorrelation  240
                res = protein.GetMoreauBrotoAuto()   
            elif jj == 5:    #Moran autocorrelation       240
                res = protein.GetMoranAuto()
            elif jj == 6:    #Geary autocorrelation       240
                res = protein.GetGearyAuto()
            elif jj == 7:    #composition,transition,distribution  21+21+105
                res = protein.GetCTD()
            elif jj == 8:    #conjoint triad features     343
                res = protein.GetTriad()
            elif jj == 9:    #sequence order coupling number  60
                res = protein.GetSOCN(30)
            elif jj == 10:   #quasi-sequence order descriptors   100
                res = protein.GetQSO()
            elif jj == 11:    #pseudo amino acid composition   50
                res = protein.GetPAAC(30)
                    
            keys.extend(res.viewkeys())
            values.extend(res.viewvalues())  
        if ii == 0:
            HP_list = keys
            D_list.append(values)
        else:
            D_list.append(values)
            
    D_Pro = np.zeros((len(D_list),len(HP_list)), dtype=float)
    for k in range(len(D_list)):
        D_Pro[k,:] = D_list[k]
        
    #Variance threshold       std > 0.01  
    import Descriptors_Selection as DesSe
    ind_var = DesSe.VarinceThreshold(D_Pro)
    D_Pro = D_Pro[:,ind_var]
    HP_list = np.array(HP_list)[ind_var]

    H_Pro = np.reshape(HP_list,(1,len(HP_list)))
    Array_Pro = np.append(H_Pro, D_Pro, axis=0) 
    
    return Array_Pro            