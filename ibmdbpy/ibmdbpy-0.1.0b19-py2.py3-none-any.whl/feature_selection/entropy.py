# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:05:39 2015

@author: efouche
"""

from numbers import Number

from ibmdbpy.internals import idadf_state

from numpy import log2

import six

@idadf_state
def entropy(idadf, target):
    data_entropy = 0.0
    count = idadf.ida_query("SELECT COUNT(*) FROM %s GROUP BY \"%s\""%(idadf.name,target))

    for value in count:
        info = value / len(idadf)
        data_entropy += ((-info) * log2(info))
    
    return data_entropy 
    
def entropy_naive2(idadf, target):
    target_values = idadf.unique(target)
    
    data_entropy = 0.0
    
    for value in target_values:
        freq = len(idadf[idadf[target] == value])
        info = freq / len(idadf)
        if info != 0: # important, otherwise may have nan 
            data_entropy += ((-info) * log2(info))
    
    return data_entropy    

#@idadf_state        
def entropy_naive1(idadf, target, disc = None):
    
    if disc is not None:
        bins = 10
        numerical_columns = idadf._get_numerical_columns()
        level_ratio = idadf.levels(target)/len(idadf)
        if (target in numerical_columns) & (level_ratio > 0.05): # arbitrary
            mini = idadf[target].min()
            maxi = idadf[target].max()   #### Problem 
            interval = (maxi - mini) / bins
            #import pdb; pdb.set_trace()
            target_values = [(mini+interval*x, mini+interval*(x+1)) for x in range(0,10)]
        else:
            target_values = idadf.unique(target)
    else:
        target_values = idadf.unique(target)
    
    data_entropy = 0.0
    
    for value in target_values:
        if isinstance(value, tuple):
            #import pdb ; pdb.set_trace()
            if value == target_values[0]:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] < value[1])])
            elif value == target_values[-1]:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] <= value[1])])
            else:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] < value[1])])
        else: 
        #if isinstance(value, six.string_types):
        #    value = "'%s'"%value
        #query = "SELECT COUNT(*) FROM %s WHERE \"%s\" = %s"%(name, target, value)
        #freq = int(idadf.ida_scalar_query(query))
        
            freq = len(idadf[idadf[target] == value])
        
        info = freq / len(idadf)
        
        if info != 0: # important, otherwise may have nan 
            data_entropy += ((-info) * log2(info))
    
    return data_entropy
    
@idadf_state   
def information_entropy_split(idadf, feature, cut, target):
    """
    SQL Pushdown computing of class information entropy of the partition of
    attribute <feature> w.r.t to cut point <cut> and target <target>
    """
    #if not isinstance(idadf, ibmdbpy.frame.IdaDataFrame):
     #   raise TypeError("idadf is not an IdaDataFrame")
    if not isinstance(feature, six.string_types):
        raise TypeError("feature is not of string type")
    if not feature in idadf:
        raise ValueError("feature does not exists in idadf")
    if not feature in idadf._get_numerical_columns():
        raise ValueError("feature does not belong to numerical attributes of idadf")
    
    if not isinstance(cut, Number):
        raise("The cut-value is not a number")
    
    if not target in idadf:
        raise ValueError("target does not exists in idadf")
    
    idadf_1 = idadf[idadf[feature] <= cut]#[[feature, target]]
    idadf_2 = idadf[idadf[feature] > cut]#[[feature, target]]
    
    if (len(idadf_1) in [0,len(idadf)]):
        feature = idadf[feature]
        raise ValueError("Invalid value for cut-value, because %s attribute range from %s to %s"
                         %(feature, feature.min(), feature.max()))
        
    entropy_1 = entropy(idadf_1, target)
    entropy_2 = entropy(idadf_2, target)
            
    return (len(idadf_1)/len(idadf))*entropy_1 + (len(idadf_2)/len(idadf))*entropy_2
