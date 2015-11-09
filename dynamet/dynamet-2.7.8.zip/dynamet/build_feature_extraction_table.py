# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:40:57 2015

@author: pkiefer
"""

import emzed
import numpy as np
from scipy import stats
from  time import time as current
from dynamet.objects_check import max_integrate
from hires import feature_regrouper, assign_adducts
from dynamet.peakmaps2feature_tables import _add_adduct_mass_shifts as adduct_mass_shifts
from dynamet import helper_funs as helper

from collections import defaultdict
#from  collections import defaultdict


def handle_parameters(parameters):
    if not parameters:
        return {'rel_min_area':0.01, 'max_c_gap':10,  'delta_mz_tolerance': 0.0008}
    else:
        keys=['delta_mz_tolerance',  'max_c_gap', 'rel_min_area']
        return {key:parameters[key] for key in keys}
        

def collect_peaks(tables, rttol, mztol):
    print 'deterimining peak maximas...'
    print 'collecting detected peaks...'
    ref=tables[0].extractColumns(*['id', 'time', 'mz', 'rt', 'area'])
    print 'initializing collection'
    collection=initial_collection(ref)
    for t in tables[1:]:
        start=current()
        print 
        print 'adding peaks of sample %s' %t.source.uniqueValue()
        comp=t.leftJoin(ref, t.mz.equals(ref.mz, abs_tol=mztol) &\
                            t.rt.equals(ref.rt, abs_tol=rttol))
        new=enlarge_collection(collection, comp, _get_id_start(ref))
        ref=update_ref_table(ref, new, collection)    
        stop=current()
        print 'Done'
        print 'took %.2fs' %(stop-start)
        print
    return ref, collection
    
def initial_collection(t):
    t.replaceColumn('id', range(len(t)), type_=int)
    collection=dict()
    update_collection(t, collection)
    _add_mz_t0(t,collection)
    return collection

def _add_mz_t0(t,collection):
    for id_, mz in zip(t.id.values, t.mz.values):
        collection[id_]['mz_t0']=mz

def enlarge_collection(collection, cand, id_start):
    print 'adding peaks to collection...'
    start=current()
    common=cand.filter(cand.id__0.isNotNone())
    common.replaceColumn('id', common.id__0, type_=int)
    new=cand.filter(cand.id__0.isNone())
    new.replaceColumn('id', range(id_start, id_start+len(new)), type_=int)
    update_collection(common, collection)
    update_collection(new, collection)
    stop=current()
    print 'Done'
    print 'took %.2fs' %(stop-start)
    return new
    
def update_collection(t, collection):
    tuples=zip(t.id.values, t.mz.values, t.rt.values, t.area.values, t.time.values)
    for id_, mz, rt, area, time in tuples:
        if collection.has_key(id_):
            collection[id_]['mz'].append(mz)
            collection[id_]['rt'].append(rt)
            collection[id_]['time'].append(time)
            collection[id_]['area']+=area
        else:
            collection[id_]={'mz':[mz], 'rt':[rt], 'time': [time], 'area':area}


def update_ref_table(ref, new, collection):
    _update_ref_table(ref, collection)
    colnames=['id', 'time', 'mz', 'rt', 'area']
    add=new.extractColumns(*colnames)
    try:
        return emzed.utils.stackTables([ref, add])
    except:
        return emzed.utils.mergeTables([ref, add], force_merge=True)
    

def _update_ref_table(ref, collection):
    def replace_(id_, key, dic=collection):
        if key=='area':
            return dic[id_][key]
        return float(np.median(dic[id_][key]))
        
    ref.replaceColumn('mz', ref.apply(replace_, (ref.id, 'mz')), type_=float)
    ref.replaceColumn('rt', ref.apply(replace_, (ref.id, 'rt')), type_=float)
    ref.replaceColumn('area', ref.apply(replace_, (ref.id, 'area')), type_=float, format_='%.2e')

def _get_id_start(ref):
    return ref.id.max()+1   
    
##################################################################################################
def get_ref_rt_var(collection):
    """ calculates rt deviations feature-wise for all features detected in at least
    3 samples and returns list
    """
    # extract rt values:
    rt_var=[]
    values=[collection[key]['rt'] for key in collection.keys()]
    for value in values:
        if len(value)>=3:
            val=[float(v-np.mean(value)) for v  in value]
            rt_var.extend(val)
    return rt_var #, 2.576*np.sqrt(sum(variability))/num

def get_typical_rt_var(collection):
    rt_var= get_ref_rt_var(collection)
    return stats.scoreatpercentile(rt_var, 95)

    
def check_ref_rttol(collection, rttol):
    rt_var= get_ref_rt_var(collection)
    quality=stats.percentileofscore(rt_var, rttol)
    if quality<90:
        print 'WARNING: high variability on retention time observed'
        return quality, 'critical'
    return quality, 'good'
##################################################################################################


def group_features(ref, rel_min_area=0.01, max_c_gap=10, rttol=10, delta_mz_tolerance=0.0008):
    _prepare_ref(ref)
    ref=feature_regrouper(ref, min_abundance=rel_min_area, max_c_gap=max_c_gap, rt_tolerance=rttol,
                      mz_tolerance=delta_mz_tolerance)
    return ref


def _prepare_ref(t):
    t.addColumn('feature_id', t.id, type_=int, insertAfter='id')
    t.addColumn('z', 0, type_=int, insertAfter='mz')

    
def add_mz_0(ref, collection):
    ref.updateColumn('feature_mz_min', ref.mz.min.group_by(ref.isotope_cluster_id), type_=float,
                  format_='%.5f')
    _move_column_after(ref, 'feature_mz_min', 'mz', float, '%.5f')
    def fun_(id_, mz, mzmin, key='mz_t0', dic=collection):
        if mz==mzmin:
            return dic.get(id_).get(key)
    ref.updateColumn('mz0', ref.apply(fun_, (ref.id, ref.mz, ref.feature_mz_min)), type_=float, 
                     format_='%.5f')              
    _move_column_after(ref, 'mz0', 'mz', float, '%.5f')
    

def _move_column_after(t,colname, after, type_, format_):
    t.addColumn(colname+'_', t.getColumn(colname), type_=type_, format_=format_, insertAfter=after)
    t.dropColumns(colname)
    t.renameColumn(colname+'_', colname)

#################################################################################################
def set_common_feature_rt(ref):
    ref.addColumn('rt_std', ref.rt.std.group_by(ref.isotope_cluster_id), type_=float)
    ref.replaceColumn('rt', ref.rt.median.group_by(ref.isotope_cluster_id), type_=float)


#################################################################################################
def remove_rare_fids(ref, collection, min_num=2):
    fid2num=_count_feature_frequency(ref, collection)
    def fun_(v, dic=fid2num):
        return len(dic[v])
    return ref.filter(ref.isotope_cluster_id.apply(fun_)>min_num)   
    
def _count_feature_frequency(ref, collection):
    d=defaultdict(set)
    pairs=zip(ref.isotope_cluster_id, ref.id)
    for fid, id_ in pairs:
            for v  in _get_time_points(id_,collection):
                d[fid].add(v)
    return d

def _get_time_points(id_,collection):
    return set(collection[id_]['time'])
##################################################################################################

def cleanup_ref(ref, isol_width, min_isotopes=2):
    # remove features with single peaks (z==0) due to repeated feature grouping
    ref=ref.filter(ref.z>0)
    ref.updateColumn('feature_mz_min', ref.mz.min.group_by(ref.isotope_cluster_id), type_=float)
    _replace_mz0(ref)
    ref=ref.filter(ref.mz-ref.feature_mz_min+isol_width>=0)
    ref.replaceColumn('feature_id', ref.isotope_cluster_id, type_=int)
    helper.get_num_isotopes(ref)
    assert len(ref)>0, 'no peaks found'
    ref=_select_for_min_isotopes(ref, min_isotopes)
    ref=remove_redundance(ref)
    ref.addEnumeration()
    helper.get_monoisotopic_mass(ref, insert_before='num_isotopes')
    return ref


def _replace_mz0(ref, delta=0.05):
    """ comments: feature_mz_min is in set(mz0.values): the feature has been recomposed and mass
        peaks of a feature with different mzmin were added.  Choose mz0 corresponding
        to feature_mz_min
    """
    icid_2_mz0=helper.extract_dict_from_table(ref, 'isotope_cluster_id', 'mz0')
    icid_2_fmzmin=helper.extract_dict_from_table(ref, 'isotope_cluster_id', 'feature_mz_min')
    def _replace(v, dic1=icid_2_mz0, dic2=icid_2_fmzmin, delta=delta):
        mz0_values=dic1[v]
        assert len(dic2[v])==1 # unique feature_mz_min
        fmzmin=dic2[v][0]
        for mz0 in mz0_values:
            if mz0:
                if abs(fmzmin-mz0)<delta:
                    return fmzmin
        return -1.0 # fix type_error
    ref.replaceColumn('mz0', ref.isotope_cluster_id.apply(_replace), type_=float)
    #fix type_error since mz0 >= 0
    ref.replaceColumn('mz0', (ref.mz0==-1.0).thenElse(None, ref.mz0), type_=float)
    
def remove_redundance(ref, collapse_names=None):
    if not collapse_names:
        collapse_names=['isotope_cluster_id', 'adduct_group', 'adduct_mass_shift',
                        'possible_adducts', 'feature_mz_min', 'rt', 'mz0', 'z', 'num_isotopes']
    delta_c=emzed.mass.C13-emzed.mass.C12
    def fun(table, row, new_col_name):
        return (table.getValue(row, 'isotope_cluster_id'), table.getValue(row, 'num_isotopes'))
    ref.addColumn('_select', fun, type_=tuple)
    # if several isotopes within same feature (this is a consequence of rttol!, peak tailing,...)
    # keep the one with hinghest area
    before=len(ref)
    ref.addColumn('a_max', ref.area.max.group_by(ref._select), type_=float)
    ref=ref.filter(ref.area==ref.a_max)
    ref.addColumn('rt_', ref.rt.median.group_by(ref.isotope_cluster_id), type_=float)
    ref.replaceColumn('rt', ref.rt_, type_=float)
    ref.dropColumns('a_max', '_select', 'rt_')
    print 'removed %d `side` peaks' %(before - len(ref))
    # constrain 2: remove features with single peaks
    before=len(ref)
    ref.addColumn('_len', ref.isotope_cluster_id.len.group_by(ref.isotope_cluster_id), type_=int)
    ref=ref.filter(ref._len>1)
    ref.dropColumns('_len')
    print 'removed %d features with only 1 peak' %(before - len(ref))
    ##################
    # COLLAPSE Table by command collapse to remove doubles and recalculate mz values based on 
    # labeled C mass shift time column 'num_isotopes'
    before=len(ref)
    ref=ref.collapse(*collapse_names)
    print 'removed %d `double` peaks' %(before - len(ref))
    ref=ref.extractColumns(*collapse_names)
    ref.addColumn('mz', ref.feature_mz_min+(ref.num_isotopes*delta_c)/(ref.z*1.0), type_=float)
    ref.renameColumns(isotope_cluster_id='feature_id')
    ref=ref.filter(ref.feature_id.len.group_by(ref.feature_id)>1)
    return ref

def _select_for_min_isotopes(t, min_isotopes):
    # Number of istopes must be equal to floor min_labeled_c
    t.addColumn('max_', t.num_isotopes.max.group_by(t.feature_id), type_=int)
    t=t.filter(t.max_>=min_isotopes)
    t.dropColumns('max_')
    return t
##################################################################################################
#  MAIN FUNCTION
#
def main_collect_and_group(tables, min_num=2, isol_width=0.003, min_isotopes=2, parameters=None):
    assert len(tables)>2, 'At least 3 samples are required'
    params=handle_parameters(parameters)
    if parameters:
        isol_width=parameters['isol_width']
        min_isotopes=parameters['min_isotopes']
    params['rttol']=helper.determine_fgrouper_rttol(tables)
    tables=[max_integrate(t) for t  in tables]
    ref, collection=collect_peaks(tables, params['rttol'], isol_width)
    try:
        f_rttol=get_typical_rt_var(collection)    
    except:
        f_rttol=isol_width
    ref_table_score=check_ref_rttol(collection, f_rttol)
    params['rttol']=f_rttol
    ref=group_features(ref, **params)
    params['ref_table_score']=ref_table_score
    add_mz_0(ref, collection)
    set_common_feature_rt(ref)
    ref=remove_rare_fids(ref, collection, min_num)
    assign_adducts(ref)
    adduct_mass_shifts(ref)
    # hires might multiply features. However feature mzmin might differ for features, and mz0
    # and feature_mz_min must be adapted
    return cleanup_ref(ref, min_isotopes)
    
    
    
    