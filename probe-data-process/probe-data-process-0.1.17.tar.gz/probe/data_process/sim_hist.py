from __future__ import absolute_import
import logging
from probe.plotting.plotting import Plotting
import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants as C
from .sim_common import SimCommon

logger = logging.getLogger(__name__)

class SimHist(SimCommon):

    def __init__(self, h5_filename):
        SimCommon.__init__(self, h5_filename)

    def hist_ari_tauc(self, bins=50, print_to_file=False, print_filename='hist_ari_tauc.eps'):

        hist, hist_edges, hist_centers = self.compute_hist('new/ari_tauc', bins=bins)

        Plotting.plot_single_ax(hist_centers, hist,
                                list_of_styles='ro', xlabel='', ylabel='ari_tauc',
                                print_to_file=print_to_file, print_filename=print_filename)

    def hist_new_all(self, particle, bins=50):

        assert particle in ['el', 'ari']

        fig, ax = plt.subplots(2, 2)

        hist, hist_edges, hist_centers = self.compute_hist('new/{}_tauc'.format(particle), bins=bins)
        ax[0, 0].plot(hist_centers, hist, 'ro')
        ax[0, 0].legend(loc='best')
        ax[0, 0].set_title('{} tauc'.format(particle))

        hist, hist_edges, hist_centers = self.compute_hist('new/{}_vx'.format(particle), bins=bins)
        ax[0, 1].plot(hist_centers, hist, 'ro')
        ax[0, 1].legend(loc='best')
        ax[0, 1].set_title('{} vx'.format(particle))

        hist, hist_edges, hist_centers = self.compute_hist('new/{}_vy'.format(particle), bins=bins)
        ax[1, 0].plot(hist_centers, hist, 'ro')
        ax[1, 0].legend(loc='best')
        ax[1, 0].set_title('{} vy'.format(particle))

        hist, hist_edges, hist_centers = self.compute_hist('new/{}_vz'.format(particle), bins=bins)
        ax[1, 1].plot(hist_centers, hist, 'ro')
        ax[1, 1].legend(loc='best')
        ax[1, 1].set_title('{} vz'.format(particle))

        plt.show()

    def compute_hist(self, dataset, bins=50, density=True):
        hist_data = self.h5_f[dataset][...]
        hist, hist_edges = np.histogram(hist_data, bins=bins, density=True)
        hist_centers = (hist_edges[:np.size(hist_edges)-1] + hist_edges[1:]) / 2.0

        return hist, hist_edges, hist_centers
