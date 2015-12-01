#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some tools for Citizen Band users

Copyright (C) 2015 by
Sébastien Celles <s.celles@gmail.com>
All rights reserved.

"""

import numpy as np
import pandas as pd
import decimal

class CitizenBand(object):
    """
    A Python class for Citizen Band users

    >>> cb = CitizenBand()
    >>> cb.frequency(19)
    Decimal('27.185')

    >>> cb.frequency(19, 1)
    Decimal('27.635')

    >>> cb.frequency(19, -1)
    Decimal('26.735')

    >>> cb.channel('26.735')
    (19, -1, Decimal('0.000'))
    """

    def __init__(self, bands=None, mask=None):
        self.nb_channels = 40
        self.channels = pd.Index(np.arange(1, self.nb_channels + 1), name='channel')


        self.band_offset = decimal.Decimal('0.450')

        if bands is None:
            bands = [-2, -1, 0, 1, 2]
            bands = [-3, -2, -1, 0, 1, 2]
        self.bands = bands
        
        freq_bands = map(lambda band: self._get_frequencies_band(band), bands)
        self._df_freq_2d = pd.concat(freq_bands, axis=1)

        if mask is None:
            mask = self._df_freq_2d < decimal.Decimal('28')
    
        self._df_freq_2d = self._df_freq_2d[mask]

        freq_bands = map(lambda band: self._get_frequencies_band(band, with_band=True), bands)
        self._df_freq_1d = pd.concat(freq_bands, axis=0)
        self._df_freq_1d = self._df_freq_1d.reset_index()

        self._fmin = self._df_freq_1d['frequency'].min()
        self._fmax = self._df_freq_1d['frequency'].max()

    def _get_frequencies_band(self, band, with_band=False):
        _frequencies = pd.Series(
            ['26.965', '26.975', '26.985', '27.005', '27.015', '27.025', '27.035', '27.055', '27.065', '27.075', 
             '27.085', '27.105', '27.115', '27.125', '27.135', '27.155', '27.165', '27.175', '27.185', '27.205', 
             '27.215', '27.225', '27.255', '27.235', '27.245', '27.265', '27.275', '27.285', '27.295', '27.305', 
             '27.315', '27.325', '27.335', '27.345', '27.355', '27.365', '27.375', '27.385', '27.395', '27.405'],
            index=self.channels, name=band)
        _frequencies = _frequencies.map(decimal.Decimal) + self.band_offset * band
        if with_band:
            _frequencies.name = 'frequency'
            _frequencies = pd.DataFrame(_frequencies)
            _frequencies['band'] = band
        return _frequencies

    @property
    def frequencies(self):
        return self._df_freq_2d

    def frequency(self, channel, band=0):
        return self._df_freq_2d.loc[channel, band]

    def channel(self, frequency):
        try:
            frequency = decimal.Decimal(frequency)
        except:
            pass
        if frequency < self._fmin or frequency > self._fmax:
            raise NotImplementedError(
                "Out of bands %s - frequency should be between [%s, %s]" 
                % (self.bands, self._fmin, self._fmax))
        self._df_freq_1d['delta_f'] = self._df_freq_1d['frequency'] - frequency
        self._df_freq_1d['abs_delta_f'] = abs(self._df_freq_1d['delta_f'])
        self._df_freq_1d = self._df_freq_1d.sort_values(by='abs_delta_f')
        res = self._df_freq_1d.iloc[0]
        return res.channel, res.band, res.delta_f

def main():
    import doctest
    doctest.testmod()

    #cb = CitizenBand()

    #print("Table of frequencies")
    #print(cb.frequencies)

    #(channel, band) = (19, 0)
    #print("Frequency of channel %d band %d" % (channel, band))
    #frequency = cb.frequency(channel, band)
    #print(frequency)

    #frequency = decimal.Decimal('28.485')
    #print("Nearest channel and band of frequency %s" % (frequency))
    #channel, band = cb.channel(frequency)
    #print(channel, band)

if __name__ == '__main__':
    main()