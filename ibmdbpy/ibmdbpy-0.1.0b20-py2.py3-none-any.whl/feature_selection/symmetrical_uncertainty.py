# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:53:19 2015

@author: efouche
"""

from collections import OrderedDict


from ibmdbpy.feature_selection import entropy
from ibmdbpy.feature_selection.private import _compute_entropy, _fill_matrix
from ibmdbpy.feature_selection.private import _check_input, _check_input_for_matrix

from ibmdbpy.internals import idadf_state
from ibmdbpy.utils import timed

#import numpy as np
#from numpy import log2
import pandas as pd
import numpy as np

import itertools

import six

@idadf_state
@timed
def su_matrix_pareto(idadf, features = None, filter_out = 0.8, version = 1):
    # Check input 
    if features is None:
        features = list(idadf.columns)
    else:
        _check_input_for_matrix(idadf, features)
     
    if version == 1:
        count_serie = idadf.count_groupby(features, count_only = True)  # ?? + target ? 
        min_count = np.floor(count_serie.quantile(filter_out))
    if version == 2:
        min_count = idadf.min_freq_of_instance(features)
    #n_records_out = count_serie[count_serie < min_count].sum() 
    ### Get data
    data = idadf.count_groupby(features, having = min_count)    
    
    values = []
    combinations = [x for x in itertools.combinations(features, 2)]
    columns_set = [{x[0], x[1]} for x in combinations]
    
    entropy_dict = dict()
    for column_pair in combinations:
        if column_pair[0] not in entropy_dict:
            entropy_dict[column_pair[0]] =  _compute_entropy(data, target=column_pair[0])
        if column_pair[1] not in entropy_dict:
            entropy_dict[column_pair[1]] =  _compute_entropy(data, target=column_pair[1])
        subset_entropy = _compute_entropy(data, target=column_pair[0], conditional=column_pair[1]) 
        gain = (entropy_dict[column_pair[0]] - subset_entropy)
        values.append(2.0 * (gain/(entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]])))
    
    ### Fill the matrix
    result = _fill_matrix(features, columns_set, values, 0.0)
    return result
    
@idadf_state
@timed
def su_pareto(idadf, target, features = None, filter_out = 0.8, version = 1):
    #import pdb ; pdb.set_trace()
    
    # Check input
    if features is None:
        features = [x for x in idadf.columns if x != target]
    else:
        if isinstance(features, six.string_types):
            features = [features]
        _check_input(idadf, target, features)

    ### determine how much data we want
    if version == 1:
        count_serie = idadf.count_groupby(features + [target], count_only = True)  # ?? + target ? 
        min_count = np.floor(count_serie.quantile(filter_out))
    if version == 2:
        min_count = idadf.min_freq_of_instance(features + [target])
    #n_records_out = count_serie[count_serie < min_count].sum() 
    ### Get data
    data = idadf.count_groupby(features + [target], having = min_count)    
    
    #return data
    
    # Compute
    value_dict = OrderedDict()
    #data_entropy = _compute_entropy(len(idadf)-n_records_out, data, target=target)
    data_entropy = _compute_entropy(data, target=target)
    
    for feature in features:
        #feature_entropy = _compute_entropy(len(idadf)-n_records_out, data, target=feature)
        feature_entropy = _compute_entropy(data, target=feature)
        #subset_entropy = _compute_entropy(len(idadf)-n_records_out, data, target=target, conditional=feature)
        subset_entropy = _compute_entropy(data, target=target, conditional=feature)
        gain = (data_entropy - subset_entropy)
        symmetrical_uncertainty = 2.0 * (gain/(data_entropy + feature_entropy))

        value_dict[feature] = symmetrical_uncertainty   
       
    # Output
    if len(features) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return symmetrical_uncertainty

@idadf_state
@timed
def su(idadf, target , features = None, having = None):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """
    # Check input
    if features is None:
        features = [x for x in idadf.columns if x != target]
    else:
        if isinstance(features, six.string_types):
            features = [features]
        _check_input(idadf, target, features)

    # Fetch data
    data = idadf.count_groupby(features + [target], having = having) 
    
    # Compute
    value_dict = OrderedDict()
    data_entropy = _compute_entropy(data, target=target)
    
    for feature in features:
        feature_entropy = _compute_entropy(data, target=feature)
        subset_entropy = _compute_entropy(data, target=target, conditional=feature)
        gain = (data_entropy - subset_entropy)
        if gain == 0: 
             value_dict[feature] = 0
        else:
            value_dict[feature] = 2.0 * (gain/(data_entropy + feature_entropy))
                
    # Output
    if len(features) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return value_dict[0]
        
@idadf_state
@timed
def su_v2(idadf, target , features = None, having = None):
    """
    Knowledge:
        su scales linearly with respect to the number of rows. 
    """
    # Check input
    if features is None:
        features = [x for x in idadf.columns if x != target]
    else:
        if isinstance(features, six.string_types):
            features = [features]
        _check_input(idadf, target, features)

    # Fetch data
    data = idadf.count_groupby([target], having = having) 
    
    # Compute
    value_dict = OrderedDict()
    data_entropy = _compute_entropy(data, target=target)
    
    for feature in features:
        data = idadf.count_groupby([feature] + [target], having = having) 
        feature_entropy = _compute_entropy(data, target=feature)
        subset_entropy = _compute_entropy(data, target=target, conditional=feature)
        gain = (data_entropy - subset_entropy)
        if gain == 0: 
             value_dict[feature] = 0
        else:
            value_dict[feature] = 2.0 * (gain/(data_entropy + feature_entropy))
                
    # Output
    if len(features) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return value_dict[0]
        
@idadf_state
@timed
def su_matrix(idadf, features = None, having = None):
    # Check input 
    if features is None:
        features = list(idadf.columns)
    else:
        _check_input_for_matrix(idadf, features)
        
    ### Get data
    data = idadf.count_groupby(features, having = having)    
    
    values = []
    combinations = [x for x in itertools.combinations(features, 2)]
    columns_set = [{x[0], x[1]} for x in combinations]
    
    entropy_dict = dict()
    for column_pair in combinations:
        if column_pair[0] not in entropy_dict:
            entropy_dict[column_pair[0]] =  _compute_entropy(data, target=column_pair[0])
        if column_pair[1] not in entropy_dict:
            entropy_dict[column_pair[1]] =  _compute_entropy(data, target=column_pair[1])
        subset_entropy = _compute_entropy(data, target=column_pair[0], conditional=column_pair[1]) 
        gain = (entropy_dict[column_pair[0]] - subset_entropy)
        if gain == 0:
            values.append(0)
        else:
            values.append(2.0 * (gain/(entropy_dict[column_pair[0]] + entropy_dict[column_pair[1]])))
    
    ### Fill the matrix
    result = _fill_matrix(features, columns_set, values, 0.0)
    return result
    

        
@idadf_state
@timed
def su_naive(idadf, target , features = None):
    # Discretize ?
    # The higher the better ?
    # tests

    if features is None:
        features = [x for x in idadf.columns if x != target]
    else:
        if isinstance(features, six.string_types):
            features = [features]
        if target in features:
            raise ValueError("target in features")
        unknown_features = []
        for feature in features:
            if feature not in idadf.columns:
                unknown_features.append("%s"%feature)
        if unknown_features:
            raise ValueError("Unknown columns: %s"%", ".join(unknown_features))

    value_dict = OrderedDict()
    
    data_entropy = entropy(idadf, target)
    
    for feature in features:
        feature_entropy = entropy(idadf, feature)
        subset_entropy = 0.0
        attr_values = idadf.unique(feature)
        #attr_values = list(attr_values[feature])
        
        #import pdb ; pdb.set_trace()
        
        for value in attr_values:
            subset = idadf[idadf[feature] == value]
            factor = len(subset)/len(idadf)
            subset_entropy += factor*entropy(subset, target)   #### += ???

        gain = (data_entropy - subset_entropy)
        #import pdb ; pdb.set_trace()
        symmetrical_uncertainty = 2.0 * (gain/(data_entropy + feature_entropy))

        value_dict[feature] = symmetrical_uncertainty   
        
    if len(features) > 1:
        result = pd.Series(value_dict)
        return result 
    else:
        return symmetrical_uncertainty