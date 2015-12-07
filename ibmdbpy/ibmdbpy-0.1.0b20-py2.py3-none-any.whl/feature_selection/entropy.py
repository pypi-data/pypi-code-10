# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:05:39 2015

@author: efouche
"""

from numbers import Number

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed


from numpy import log, log2

import six

@idadf_state
#@timed
def entropy(idadf, target, conditional = None, version = 2, log2 = True, execute = True):
    """
    v2 is the best
    
    check if v3 performs worst on a bigger sql machine
    -> slightly better if not
    
    question : v3 -> Overflow risk ? 
    """
    length = len(idadf)
    
    if isinstance(target, six.string_types):
        target = [target]
    if isinstance(conditional, six.string_types):
        conditional = [conditional]
    
    log2str = ''
    if log2 is True:
        log2str = "/LOG(2)"
         
    if not conditional:
        targetstr = "\",\"".join(target)
        if version == 1:
            subquery = "SELECT CAST(COUNT(*) AS FLOAT)/%s AS count FROM %s GROUP BY \"%s\""%(length, idadf.name,targetstr)
            query = "SELECT SUM(-count*LOG(count))%s as ent FROM (%s)"%(log2str, subquery)
            if not execute:
                return query
            return idadf.ida_scalar_query(query)
        if version == 2:
            subquery = "SELECT CAST(COUNT(*) AS FLOAT) AS count FROM %s GROUP BY \"%s\""%(idadf.name,targetstr)
            query = "SELECT (SUM(-count*LOG(count))/%s + LOG(%s))%s as ent FROM (%s)"%(length, length, log2str, subquery)
            if not execute:
                return query
            return idadf.ida_scalar_query(query)
        if version == 3: # lightweight
            subquery = "SELECT CAST(COUNT(*) AS FLOAT) AS count FROM %s GROUP BY \"%s\""%(idadf.name,targetstr)
            #query = "SELECT SUM(-count*LOG(count))%s as ent FROM (%s)"%(log2str, subquery)
            query = "SELECT SUM(-count*LOG(count)) as ent FROM (%s)"%(subquery)
            if not execute:
                # do not include the normalisation (/N + log(N)/)log(2) because it is assumed that it will be included in futher calculus
                return query
            
            result = idadf.ida_scalar_query(query)
            #result = (result / length) + log(length)
            #if log2:
            #    return result / log(2)
            return result
    else:
        if version == 1:
            conditionalstr = "\",\"".join(conditional)
            condition = " AND ".join(["A.\"%s\" = B.\"%s\""%(cond,cond) for cond in conditional])
            atarget = ", ".join(["A.\"%s\""%(tar) for tar in target])
            aconditional = ", ".join(["A.\"%s\""%(cond) for cond in conditional if cond not in target])
            groupbystr = ", ".join([atarget , aconditional, "COUNT1"])
            if not aconditional:
                groupbystr = ", ".join([atarget, "COUNT1"])
            subsubquery = "(SELECT \"%s\",CAST(count(*) AS FLOAT) as COUNT1 FROM %s GROUP BY \"%s\")"%(conditionalstr, idadf.name, conditionalstr)
            subquery = ("SELECT B.COUNT1, CAST(count(*) AS FLOAT) as COUNT2 FROM %s AS A "+
                        "INNER JOIN (%s) AS B ON %s GROUP BY %s")%(idadf.name, subsubquery, condition, groupbystr)
            query = "SELECT (SUM(COUNT2*LOG(COUNT1/COUNT2))%s)/%s FROM (%s)"%(log2str, length, subquery)
            if not execute:
                return query            
            
        if version == 2:
            ent1 = entropy(idadf, target + conditional, log2=False, execute = False)
            ent2 = entropy(idadf, conditional, log2=False, execute = False)
            query = "SELECT (MAX(ent) - MIN(ent))%s FROM (%s)"%(log2str, " UNION ALL ".join([ent1,ent2]))
            if not execute:
                return query    
        
        return idadf.ida_scalar_query(query)
    
    
@idadf_state
def entropy_naive3(idadf, target):
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
    if isinstance(target, list):
        target = target[0]
    
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
            if value == target_values[0]:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] < value[1])])
            elif value == target_values[-1]:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] <= value[1])])
            else:
                freq = len(idadf[(idadf[target] >= value[0])&(idadf[target] < value[1])])
        else: 
        
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
