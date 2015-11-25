# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 08:59:00 2015

@author: efouche
"""

from collections import OrderedDict

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

import pandas as pd
from numpy import log2

import itertools

import six

#from ibmdbpy.feature_selection import discretize
from ibmdbpy.feature_selection.discretize import discretize

from ibmdbpy.feature_selection.private import _compute_entropy, _fill_matrix
from ibmdbpy.feature_selection.private import _check_input, _check_input_for_matrix


@idadf_state
@timed
def info_gain_matrix(idadf, features = None):
    # Check input 
    if features is None:
        features = list(idadf.columns)
    else:
        _check_input_for_matrix(idadf, features)
           
    ### Get data
    data = idadf.count_groupby(features)    
    
    values = []
    combinations = [x for x in itertools.combinations(features, 2)]
    columns_set = [{x[0], x[1]} for x in combinations]

    entropy_dict = dict()
    
    ### Compute
    for column_pair in combinations:
        if column_pair[0] not in entropy_dict:
            entropy_dict[column_pair[0]] =  _compute_entropy(idadf, data, target=column_pair[0])
        subset_entropy = _compute_entropy(idadf, data, target=column_pair[0], conditional=column_pair[1])            
        values.append(entropy_dict[column_pair[0]] - subset_entropy)
    
    ### Fill the matrix
    result = _fill_matrix(features, columns_set, values, 0.0)
    return result

@idadf_state
@timed
def info_gain(idadf, target, features = None):
    # Check input
    if features is None:
        features = [x for x in idadf.columns if x != target]
    else:
        _check_input(idadf, target, features)
      
    # Fetch data 
    data = idadf.count_groupby(features + [target])   
    
    # Compute
    value_dict = OrderedDict()
    data_entropy = _compute_entropy(idadf, data, target=target)
    
    for feature in features: 
        subset_entropy = _compute_entropy(idadf, data, target=target, conditional=feature)  
        value_dict[feature] = data_entropy - subset_entropy
    
    # Output
    if len(features) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return value_dict[features[0]]

        
@idadf_state
@timed
def info_gain_disc(idadf, target, featurelist = None, disc = False):
    ###########################################################################
    def _info_gain():    
        value_dict = OrderedDict()
    
        feature_str = "\",\"".join(featurelist)
        data = idadf.ida_query("SELECT \"%s\", \"%s\", COUNT(*) AS \"count\" FROM %s GROUP BY \"%s\", \"%s\""%(feature_str,target,tablename,feature_str,target))
        
        data_entropy = _compute_entropy(idadf, data, target=target)
        #target_count = data.pivot_table(index = target, aggfunc = "sum")['count']
    
        #data_entropy = 0.0
        #for value in target_count:
        #    info = value / len(idadf)
        #    data_entropy += ((-info) * log2(info))
        
        for feature in featurelist: 
            subset_entropy = _compute_entropy(idadf, data, target=target, conditional=feature)
            #subset_entropy = 0.0
            #print(data)
            #feature_count = data.pivot_table(index = feature.lower(), aggfunc = "sum")['count']   ### TEMP LOWER
            #cond_feature_count = data.pivot_table(index = [feature.lower(), target], aggfunc = "sum")['count']
          
            #for value in cond_feature_count.index.levels[0]:
            #    cond_count = cond_feature_count[value]
            #    factor = feature_count[value]/len(idadf)
            #    subentropy = 0.0
            #    for val in cond_count:
            #        info = val / feature_count[value]
            #        subentropy += ((-info) * log2(info))
                
            #    subset_entropy += factor*subentropy
                
            value_dict[feature] = data_entropy - subset_entropy
        
        if len(featurelist) > 1:
            result = pd.Series(value_dict)
            return result 
        else:
            return value_dict[featurelist[0]]
    ###########################################################################
            
    if featurelist is None:
        featurelist = [x for x in idadf.columns if x != target]
    else:
        if isinstance(featurelist, six.string_types):
            featurelist = [featurelist]
        if target in featurelist:
            raise ValueError("target in featurelist")

    if disc is True:
        numerical_columns = idadf._get_numerical_columns()
        col = [x for x in featurelist if x in numerical_columns]
        tablename = idadf.name
        if any(col):
            try:
                tablename = discretize(idadf, columnlist = col, target = target, disc = "em")
                result = _info_gain()
            except:
                raise
            finally:
                if tablename != idadf.name:
                    idadf._idadb.drop_table(tablename)
            return result
    else:
        tablename = idadf.name
        return _info_gain()
        
    
        
@idadf_state
@timed
def info_gain_naive2(idadf, target, feature_list = None):
    # Discretize ?
    # The higher the better 
    # tests
        
    if feature_list is None:
        feature_list = [x for x in idadf.columns if x != target]
    else:
        if isinstance(feature_list, six.string_types):
            feature_list = [feature_list]
        # make sure the target is not in feature_list
        if target in feature_list:
            feature_list = [x for x in feature_list if x != target]

    value_dict = OrderedDict()
    
    data_entropy = 0.0
    data = idadf.ida_query("SELECT \"%s\", COUNT(*) FROM %s GROUP BY \"%s\""%(target,idadf.name,target))
    count = data[data.columns[-1]]
    count.index = data[data.columns[0]]
    for value in count:
        info = value / len(idadf)
        data_entropy += ((-info) * log2(info))
    
    for feature in feature_list:
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
    
    if len(feature_list) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return value_dict[feature_list[0]]

from ibmdbpy.feature_selection.entropy import entropy_naive1
     
@idadf_state
@timed
def info_gain_naive1(idadf, target, feature_list = None):
    # Discretize ?
    # The higher the better 
    # tests
        
    if feature_list is None:
        feature_list = [x for x in idadf.columns if x != target]
    else:
        if isinstance(feature_list, six.string_types):
            feature_list = [feature_list]
        # make sure the target is not in feature_list
        if target in feature_list:
            feature_list = [x for x in feature_list if x != target]

    #name = idadf.internal_state.current_state

    value_dict = OrderedDict()
    
    data_entropy = entropy_naive1(idadf, target)
    
    for feature in feature_list:
        subset_entropy = 0.0
        #attr_values = idadf.ida_query("SELECT DISTINCT \"%s\" FROM %s"%(feature, name))
        #attr_values = list(attr_values[feature])
        attr_values = idadf.unique(feature)
        
        for value in attr_values:
            subset = idadf[idadf[feature] == value]
            factor = len(subset)/len(idadf)
            subset_entropy += factor*entropy_naive1(subset, target)
            print("feature %s : value %s : factor %s : subentropy %s"%(feature, value, factor, subset_entropy))
            
        value_dict[feature] = data_entropy - subset_entropy
    
    if len(feature_list) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return value_dict[feature_list[0]]