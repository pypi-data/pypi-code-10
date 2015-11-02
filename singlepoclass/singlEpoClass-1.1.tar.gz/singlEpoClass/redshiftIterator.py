import glob
import gzip
import cPickle as pickle
import numpy as np
from photoz import find_photo_z
from randomForest import obtain_proba
from survivalFunc import find_percentile


def iterator(type, my_dir, file_dir, filter1, filter2, filter3,
             flux_filter1, flux_filter2, flux_filter3, flux_filter1_err,
             flux_filter2_err, flux_filter3_err, photo_z_type=None,
             photo_z_file=None, photo_z_redshift_file=None, mu=None,
             sigma=None):
    ''' type: RF (random forest)
              survival (survival function)
              photo_z
    '''
    files = []
    my_z = []
    quant = []
    my_files = glob.glob(my_dir + file_dir + '*simulated*.gz')
    files.append(sorted(my_files))

    for a in files[0]:
        min_index = a.index('/z') + 2
        my_z.append(a[min_index:min_index + 3])
    z = np.asarray(my_z, dtype=int)
    z = np.divide(z, 100.)

    if type == 'RF':
        for i in range(len(files[0])):
            RF = obtain_proba(
              my_dir, file_dir, filter1, filter2, filter3, flux_filter1,
              flux_filter2, flux_filter3, flux_filter1_err, flux_filter2_err,
              flux_filter3_err, z[i])[0]
            quant.append(RF)

    elif type == 'survival':
        for i in range(len(files[0])):
            survival_f = find_percentile(my_dir, file_dir, filter1, filter2,
                                         filter3, flux_filter1, flux_filter2,
                                         flux_filter3, flux_filter1_err,
                                         flux_filter2_err, flux_filter3_err,
                                         z[i])
            quant.append(survival_f)

    elif type == 'photo_z':
        if photo_z_type == 'file':
            photo_z_file = photo_z_file
            photo_z = find_photo_z(photo_z_type, photo_z_file,
                                   photo_z_redshift_file, z, mu, sigma)
        elif photo_z_type == 'gauss':
            photo_z = find_photo_z(photo_z_type, photo_z_file,
                                   photo_z_redshift_file, z, mu, sigma)
        quant = np.asarray(photo_z)
    return (quant, z)


def save_file(object, filename, protocol=-1):
    """Saves a compressed object to disk"""
    file = gzip.GzipFile(filename, 'wb')
    pickle.dump(object, file, protocol)
    file.close()
    return ()


def save_arrays(my_dir, file_dir, filter1, filter2, filter3, flux_filter1,
                flux_filter2, flux_filter3, flux_filter1_err,
                flux_filter2_err, flux_filter3_err, outdir):

    rf, rf_z = iterator('RF', my_dir, file_dir, filter1, filter2, filter3,
                        flux_filter1, flux_filter2, flux_filter3,
                        flux_filter1_err, flux_filter2_err, flux_filter3_err)

    sf, sf_z = iterator('survival', my_dir, file_dir, filter1, filter2,
                        filter3, flux_filter1, flux_filter2, flux_filter3,
                        flux_filter1_err, flux_filter2_err, flux_filter3_err)

    keys = ['rf', 'rf_z',
            'sf', 'sf_z',
            ]
    values = [rf, rf_z, sf, sf_z]

    my_dict = dict(zip(keys, values))
    file_name = outdir + 'random-forest_survival-function.p'
    save_file(my_dict, file_name)
    return file_name
