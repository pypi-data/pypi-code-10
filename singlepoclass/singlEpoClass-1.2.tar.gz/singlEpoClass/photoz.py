import numpy as np
from scipy import io, interpolate, stats


def find_photo_z(type, file=None, file_z=None, z=None, mu=None,
                 sigma=None):
    """Type: file or gauss
       Note: file_z implementation NOT tested.
    """

    if type == 'file':
        pz_file = io.readsav(file)
        pz = pz_file['p_z']
        if file_z is not None:
            my_z = io.readsav(file_z)
            my_z = my_z['z']
        else:
            my_z = np.arange(0, 5, .01)
        if np.shape(pz) != np.shape(my_z):
            raise ValueError("pz array and z array are different sizes!")
        func_my_photo_z = interpolate.interp1d(my_z, pz)
        my_photo_z = func_my_photo_z(z)
        my_photo_z = np.asarray(my_photo_z/my_photo_z.max())

    elif type == 'gauss':
        my_photo_z = stats.norm.pdf(z, mu, sigma)
        my_photo_z = np.asarray(my_photo_z/my_photo_z.max())
    return my_photo_z
