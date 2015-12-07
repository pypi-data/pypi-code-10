# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 08:59:00 2015

@author: efouche
"""

from collections import OrderedDict

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

import pandas as pd
from numpy import log2, log

import itertools

import six

#from ibmdbpy.feature_selection import discretize
from ibmdbpy.feature_selection.entropy import entropy

from ibmdbpy.feature_selection.private import _compute_entropy, _fill_matrix

@idadf_state
@timed
def info_gain(idadf, target = None, features = None, mode = "hybrid", version = 1):
    """
    To experiment as matrix with respect to info_gain
    """
    # Check input
    if target is not None:
        if not isinstance(target, six.string_types):
            raise ValueError("target should be a string")
        if target not in idadf.columns:
            raise ValueError("Unknown column %s"%target)
    
    if features is not None:
        if isinstance(features, six.string_types):
            features = [features]
        for x in features:
            if x not in idadf.columns:
                raise ValueError("Unknown column %s"%x)
    else:
        if target is not None:
            features = [x for x in idadf.columns if x not in target]
        else:
            features = list(idadf.columns)
        
    if target is not None : # Do not compute the matrix
        if mode == "python3":
            result = _info_gain_python3(idadf, target, features)
        elif mode == "python2":
            result = _info_gain_python2(idadf, target, features)
        elif mode == "python1":
            result = _info_gain_python1(idadf, target, features)
        elif mode == "hybrid":
            result = _info_gain_hybrid(idadf, target, features, version = version)
        elif mode == "sql1":
            result = _info_gain_sql1(idadf, target, features)
        elif mode == "sql2":
            result = _info_gain_sql2(idadf, target, features)
        else:
            raise NotImplementedError("Unknown mode")
    else:
        if mode == "python1":
            result = _info_gain_matrix_python1(idadf, features)
        elif mode == "hybrid":
            values = []
            combinations = [x for x in itertools.combinations(features, 2)]
            columns_set = [{x[0], x[1]} for x in combinations]
    
            entropy_dict = dict()   
            
            ### Compute
            for column_pair in combinations:
                if column_pair[0] not in entropy_dict:
                    entropy_dict[column_pair[0]] = entropy(idadf, column_pair[0])
                if column_pair[1] not in entropy_dict:
                    entropy_dict[column_pair[1]] = entropy(idadf, column_pair[1])
                join_entropy =entropy(idadf,  [column_pair[0]] + [column_pair[1]])            
                values.append(entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]] - join_entropy)
        
            ### Fill the matrix
            result = _fill_matrix(features, columns_set, values, 0.0)
        else:
            raise NotImplementedError("Unknown mode")
    
    if isinstance(result, pd.Series):
        if len(result) == 1:
            return result[0]
        else:
            result.sort(ascending = False)
            
    return result

def _add_constant(selectstr, constant, asclause):
    asclause = 'as %s'%asclause
    return "SELECT '%s' %s,"%(constant, asclause) + selectstr[6:]

def _info_gain_hybrid(idadf, target, features, version):
    entropy_dict = OrderedDict()
            
    target_entropy = entropy(idadf, target, log2 = False, version = version)
    for feature in features:
        if feature not in entropy_dict:
            entropy_dict[feature] = entropy(idadf, feature, log2 = False, version = version)
        join_entropy = entropy(idadf, [target] + [feature], log2 = False, version = version)
        
        if version == 3:
            length = len(idadf)
            entropy_dict[feature] = ((target_entropy + entropy_dict[feature] - join_entropy)/length + log(length))/log(2)
        else:
            entropy_dict[feature] = (target_entropy + entropy_dict[feature] - join_entropy)/log(2)
        
    return pd.Series(entropy_dict)
    

def _info_gain_sql1(idadf, target, features):
    entropylist = []
    target_entropy = entropy(idadf, target, log2 = False)
    
    ######################################################
    for feature in features: 
        entropystr = entropy(idadf, feature, log2 = False, execute = False)
        entropystr = _add_constant(entropystr, feature, "column")
        entropylist.append(entropystr)
    query = " UNION ALL ".join(entropylist)
    
    entropy1 = idadf.ida_query(query)
    entropy1_serie = entropy1['ent']
    entropy1_serie.index = entropy1['column']
    
    #######################################################
    iglist = []
    for feature in features:
        igstr = entropy(idadf, [feature] + [target], log2 = False, execute = False)
        igstr = _add_constant(igstr, feature, "column")
        iglist.append(igstr)
    query = " UNION ALL ".join(iglist)
    
    ig = idadf.ida_query(query)
    ig_serie = ig['ent']
    ig_serie.index = ig['column']
    
    result = pd.Series()
    for value in ig_serie.index:
        result[value] = (entropy1_serie[value] + target_entropy - ig_serie[value])/log(2)
    
    return result
    
def _info_gain_sql2(idadf, target, features):
    entropylist = []
    target_entropy = entropy(idadf, target, log2 = False)
    
    ######################################################
    for feature in features: 
        entropystr = entropy(idadf, feature, log2 = False, execute = False)
        entropystr = _add_constant(entropystr, feature, "column")
        entropylist.append(entropystr)
    query = " UNION ALL ".join(entropylist)
    
    entropy1 = idadf.ida_query(query)
    entropy1_serie = entropy1['ent']
    entropy1_serie.index = entropy1['column']
    
    #######################################################
    iglist = []
    for feature in features:
        joinstr = entropy(idadf, [feature] + [target], log2 = False, execute = False)
        igstr = "SELECT (%s + %s - SUM(-count*LOG(count)))/LOG(2) as ent"%(target_entropy, entropy1_serie[feature]) + joinstr[36:]
        igstr = _add_constant(igstr, feature, "column")
        iglist.append(igstr)
    query = " UNION ALL ".join(iglist)
    query = query + " ORDER BY \"ENT\" DESC"
    
    ig = idadf.ida_query(query)
    ig_serie = ig['ent']
    ig_serie.index = ig['column']
    
    return ig_serie.copy()

def _info_gain_python1(idadf, target, features):            
    # Get data 
    data = idadf.count_groupby(features + [target])   
        
    # Compute
    value_dict = OrderedDict()
    data_entropy = _compute_entropy(data, target=target)
    
    for feature in features: 
        subset_entropy = _compute_entropy(data, target=target, conditional=feature)  
        value_dict[feature] = data_entropy - subset_entropy
    
    return pd.Series(value_dict)
        
def _info_gain_matrix_python1(idadf, features):
    ### Get data
    data = idadf.count_groupby(features)    

    values = []
    combinations = [x for x in itertools.combinations(features, 2)]
    columns_set = [{x[0], x[1]} for x in combinations]

    entropy_dict = dict()
    
    ### Compute
    for column_pair in combinations:
        if column_pair[0] not in entropy_dict:
            entropy_dict[column_pair[0]] =  _compute_entropy(data, target=column_pair[0])
        subset_entropy = _compute_entropy(data, target=column_pair[0], conditional=column_pair[1])            
        values.append(entropy_dict[column_pair[0]] - subset_entropy)

    ### Fill the matrix
    result = _fill_matrix(features, columns_set, values, 0.0)
    return result  
        
def _info_gain_python2(idadf, target, features):
    value_dict = OrderedDict()
    
    data_entropy = 0.0
    data = idadf.ida_query("SELECT \"%s\", COUNT(*) FROM %s GROUP BY \"%s\""%(target,idadf.name,target))
    count = data[data.columns[-1]]
    count.index = data[data.columns[0]]
    for value in count:
        info = value / len(idadf)
        data_entropy += ((-info) * log2(info))
    
    for feature in features:
        subset_entropy = 0.0               
        
        data = idadf.ida_query("SELECT \"%s\",  \"%s\", COUNT(*) AS \"count\" FROM %s GROUP BY \"%s\", \"%s\""%(feature,target,idadf.name,feature,target))
        count_1 = data.pivot_table(index = data.columns[0], aggfunc = "sum")['count']
        count_2 = data.pivot_table(index = [data.columns[0], data.columns[1]], aggfunc = "sum")['count']
        
        for value in count_2.index.levels[0]:
            data = count_2[value]
            factor = count_1[value]/len(idadf)
            subentropy = 0.0
            for value_2 in data:
                info = value_2 / count_1[value]
                subentropy += ((-info) * log2(info))
                        
            subset_entropy += factor*subentropy

        value_dict[feature] = data_entropy - subset_entropy
    
    return pd.Series(value_dict)
    
def _info_gain_python3(idadf, target, features):
    from ibmdbpy.feature_selection.entropy import entropy_naive1, entropy_naive2, entropy_naive3
    value_dict = OrderedDict()
    
    data_entropy = entropy(idadf, target)
    
    for feature in features:
        subset_entropy = 0.0
        attr_values = idadf.unique(feature)
        
        for value in attr_values:
            subset = idadf[idadf[feature] == value]
            factor = len(subset)/len(idadf)
            subset_entropy += factor*entropy(subset, target)
            #print("feature %s : value %s : factor %s : subentropy %s"%(feature, value, factor, subset_entropy))
            
        value_dict[feature] = data_entropy - subset_entropy
    
    return pd.Series(value_dict)
