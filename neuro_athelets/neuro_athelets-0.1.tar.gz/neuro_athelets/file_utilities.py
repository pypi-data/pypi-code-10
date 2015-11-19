# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 09:48:28 2014

@author: leoliu
"""

#not used
def getFileNames():
    import glob
    from os.path import isfile
    file_list = glob.glob('./*.ahdr')
    fTrueName = ''
    for fileName in file_list:
        fTrueName = fileName[:-5]
        if isfile(fTrueName):
            print 'it is there'

#e.g. if i have '../Victoria_Azarenka/Victoria_Azarenka.TXT' then it goes to Victoria_Azarenka
def getNameFromFile(fName):
    return fName.split('/')[-1].split('.')[0]

#get the file names *_data.txt from folder
def getNamesFromFolder(fName):
    import glob
    return glob.glob(fName+'/*_data.txt')


#edf indicates if the file is from edf or not
def readTxt(fName,edf = False):
    import os
    import sys
    import numpy as np
    if not os.path.exists(fName):
        print('ERROR: file %s was not found!' % fName)
        return []
    print 'opening file'+fName
    f = open(fName,'r')
    data =[]
    i=0
    for line in f:
        i+=1
        try:
            line = line.replace(',',' ')
            splitted = np.array(line.split())
            splitted.astype(np.float)
            if edf:
                #eating the first line because thats the time
                data.append(splitted[1:])
            else:
                data.append(splitted)
        except ValueError:
            print('eating a line because of value error which might mean a line contains String at line: %d'%i)
            continue
    data = np.array(data)
    print len(data)
    print len(data[0])
    print data.dtype
    f.close()
    data = data.T.astype(np.float)
    return data

#for getattr to use. 
def getPlugIn():
    return {}

def createFolder(folderPath):
    import os
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
def readYaml(fName):
    import yaml
    try:
        with open(fName,'r') as f:
            data = yaml.load(f)

        return data
    except Exception as e:
        print e
        
