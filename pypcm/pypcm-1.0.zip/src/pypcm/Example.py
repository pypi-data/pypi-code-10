# -*- coding: utf-8 -*-
"""
Created on Wed Sep 09 13:37:41 2015

@author: user01
"""

def main():
    print "An example for implementing QP_SAR workflow using QSAR data with default parameters"
    import os 
    p = os.environ
    path = p['CONDA_ENV_PATH']
    path_QSAR = path+'/Lib/site-packages/QP_SAR/QSAR_data'
    
    import Initial as ini
    user = ini.userdefined(path_QSAR,'AI',Ligand_index=[1], Iteration=10, NumPermute=10)    
    ini.Run(user) 

if __name__ == '__main__':
    main()