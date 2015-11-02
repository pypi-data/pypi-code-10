import copy
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from funcsForSimulatedData import load, file_name, add_error


def get_data(my_dir, file_dir, filter1, filter2, filter3, flux_filter1_err,
             flux_filter2_err, flux_filter3_err, z):

    indices = [i for i, x in enumerate(file_dir) if x == '_']
    n = int(file_dir[1:indices[0]])
    n_Ibc_start = int(n)
    n_II_start = 2 * n_Ibc_start

    mc_file_name = file_name(my_dir, file_dir, z)
    mc_dict = load(mc_file_name)
    mc_dict = add_error(mc_dict, filter1, flux_filter1_err)
    mc_dict = add_error(mc_dict, filter2, flux_filter2_err)
    mc_dict = add_error(mc_dict, filter3, flux_filter3_err)

    all_filter1 = np.concatenate(
                (mc_dict['type_Ia']['flux'][filter1],
                 mc_dict['type_Ibc']['flux'][filter1],
                 mc_dict['type_II']['flux'][filter1]))

    all_filter2 = np.concatenate(
                (mc_dict['type_Ia']['flux'][filter2],
                 mc_dict['type_Ibc']['flux'][filter2],
                 mc_dict['type_II']['flux'][filter2]))

    all_filter3 = np.concatenate(
                (mc_dict['type_Ia']['flux'][filter3],
                 mc_dict['type_Ibc']['flux'][filter3],
                 mc_dict['type_II']['flux'][filter3]))

    data = [all_filter1, all_filter2, all_filter3]
    data = zip(*data)
    all_sources = pd.DataFrame(data, columns=[filter1, filter2, filter3],
                               index=range(3*n))
    all_sources['Type'] = 'Type Ia'
    all_sources.ix[n_Ibc_start:n_II_start, 'Type'] = 'Type Ibc'
    all_sources.ix[n_II_start:, 'Type'] = 'Type II'
    all_features = copy.copy(all_sources)
    all_label = all_sources["Type"]
    del all_features["Type"]

    X = copy.copy(all_features.values)
    Y = copy.copy(all_label.values)

    return X, Y


def obtain_proba(my_dir, file_dir, filter1, filter2, filter3, flux_filter1,
                 flux_filter2, flux_filter3, flux_filter1_err,
                 flux_filter2_err, flux_filter3_err, z):

    X, Y = get_data(my_dir, file_dir, filter1, filter2, filter3,
                    flux_filter1_err, flux_filter2_err, flux_filter3_err, z)

    Y[Y == "Type Ia"] = 0
    Y[Y == "Type Ibc"] = 1
    Y[Y == "Type II"] = 2
    Y = Y.astype(int)

    clf = RandomForestClassifier(n_estimators=200, oob_score=True)
    rfc = clf.fit(X, Y)
    proba = rfc.predict_proba([flux_filter1, flux_filter2, flux_filter3])
    return(proba)
