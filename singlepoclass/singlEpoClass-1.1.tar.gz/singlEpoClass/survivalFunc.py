import numpy as np
from sklearn.neighbors import KernelDensity
from funcsForSimulatedData import load, file_name, add_error


def kde3d(x, y, z, data_point):
    values = np.vstack([x, y, z]).T
    # Use grid search cross-validation to optimize the bandwidth
    # params = {'bandwidth': np.logspace(-1, 1, 20)}
    kde = KernelDensity(bandwidth=0.3)
    kde.fit(values)
    kde_coords = kde.sample(10000)
    log_pdf = kde.score_samples(kde_coords)
    percentile = np.sum(log_pdf < kde.score(data_point))/10000.
    return (percentile)


def find_percentile(my_dir, file_dir, filter1, filter2, filter3, flux_filter1,
                    flux_filter2, flux_filter3, flux_filter1_err,
                    flux_filter2_err, flux_filter3_err, z):

    all_percentile = []
    data_point = (flux_filter1, flux_filter2, flux_filter3)
    data_point = np.asarray(data_point)

    mc_file_name = file_name(my_dir, file_dir, z)
    mc_dict = load(mc_file_name)
    mc_dict = add_error(mc_dict, filter1, flux_filter1_err)
    mc_dict = add_error(mc_dict, filter2, flux_filter2_err)
    mc_dict = add_error(mc_dict, filter3, flux_filter3_err)

    print 'redshift: ', z

    Ia_percentile = kde3d(mc_dict['type_Ia']['flux'][filter1],
                          mc_dict['type_Ia']['flux'][filter2],
                          mc_dict['type_Ia']['flux'][filter3], data_point)

    Ibc_percentile = kde3d(mc_dict['type_Ibc']['flux'][filter1],
                           mc_dict['type_Ibc']['flux'][filter2],
                           mc_dict['type_Ibc']['flux'][filter3], data_point)

    II_percentile = kde3d(mc_dict['type_II']['flux'][filter1],
                          mc_dict['type_II']['flux'][filter2],
                          mc_dict['type_II']['flux'][filter3], data_point)

    my_percentile = (Ia_percentile, Ibc_percentile, II_percentile)
    my_percentile = np.asarray(my_percentile)
    all_percentile.append(my_percentile)
    all_percentile = np.squeeze(all_percentile)

    return all_percentile
