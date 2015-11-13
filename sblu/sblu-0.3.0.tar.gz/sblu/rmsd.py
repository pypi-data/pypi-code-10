import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform


def rmsd(x, y):
    delta = x - y
    N = len(delta)
    np.multiply(delta, delta, delta)
    return np.sqrt((delta.sum() / N))


def interface(rec, lig, interface_d):
    dists = cdist(rec._getCoords(), lig._getCoords(), 'sqeuclidean')
    indices = np.any(dists < (interface_d * interface_d), axis=0).nonzero()[0]
    return indices


def calc_rmsd(ag, ref, interface=None):
    if interface is not None:
        pass


def interface_pwrmsd(rec, lig, interface_d=10.0, condensed=False):
    transformed = lig._getCoordsets()
    N = lig.numCoordsets()

    interfaces = [interface(rec._getCoords(), coords, 10.0)
                  for coords in transformed]

    dists = np.zeros((N, N), dtype=np.float64)
    for i in range(N):
        for j in range(i, N):
            combined_interface = np.union1d(interfaces[i], interfaces[j])
            if len(combined_interface) == 0:
                d = -1
            else:
                d = rmsd(transformed[i][combined_interface],
                         transformed[j][combined_interface])
            dists[i, j] = dists[j, i] = d

    if condensed:
        return squareform(dists)
    return dists


def pwrmsd(lig, condensed=False):
    N = lig.numCoordsets()

    condensed_dists = pdist(lig._getCoordsets().reshape(N, -1), 'sqeuclidean')
    np.divide(condensed_dists, lig.numAtoms(), condensed_dists)
    np.sqrt(condensed_dists, condensed_dists)
    if not condensed:
        return squareform(condensed_dists)
    return condensed_dists
