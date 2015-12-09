########################################################
# Started Logging At: 2015-11-07 14:54:48
########################################################

sp = pyspeckit.Spectrum('sn2009ip_halpha.fits')
import pyspeckit
sp = pyspeckit.Spectrum('sn2009ip_halpha.fits')
sp.plotter(figure=pl.figure(1))
sp.specfit(plot=True, fittype='voigt')
sp.specfit(plot=True, fittype='voigt')
sp.plotter(xmin=6300, xmax=6700)
sp.specfit(plot=True, fittype='voigt')
fwhm = sp.specfit.measure_approximate_fwhm(threshold='error', emission=True, interpolate_factor=1024, plot=True, grow_threshold=1)
get_ipython().magic('debug')
get_ipython().magic('history ')
########################################################
# Started Logging At: 2015-11-07 14:57:42
########################################################

import pyspeckit
sp = pyspeckit.Spectrum('sn2009ip_halpha.fits')
sp.plotter(xmin=6300, xmax=6700)
sp.specfit(plot=True, fittype='voigt')
fwhm = sp.specfit.measure_approximate_fwhm(threshold='error', emission=True, interpolate_factor=1024, plot=True, grow_threshold=1)
np.seterr(invalid='raise')
fwhm = sp.specfit.measure_approximate_fwhm(threshold='error', emission=True, interpolate_factor=1024, plot=True, grow_threshold=1)
np.seterr('raise')
fwhm = sp.specfit.measure_approximate_fwhm(threshold='error', emission=True, interpolate_factor=1024, plot=True, grow_threshold=1)
########################################################
# Started Logging At: 2015-11-07 15:04:24
########################################################

sp = pyspeckit.Spectrum('sn2009ip_halpha.fits')
import pyspeckit
sp = pyspeckit.Spectrum('sn2009ip_halpha.fits')
sp.data = 1-sp.data
sp.plotter(xmin=6300, xmax=6700)
sp = pyspeckit.Spectrum('sn2009ip_halpha.fits')
sp.data = 2-sp.data
sp.plotter(xmin=6300, xmax=6700)
sp.specfit(plot=True, fittype='voigt')
sp.plotter(xmin=6300, xmax=6700)
sp.specfit(plot=True, fittype='voigt')
fwhm = sp.specfit.measure_approximate_fwhm(threshold='error', emission=True, interpolate_factor=1024, plot=True, grow_threshold=1)
fwhm = sp.specfit.measure_approximate_fwhm(threshold='error', emission=False, interpolate_factor=1024, plot=True, grow_threshold=1)
fwhm
########################################################
# Started Logging At: 2015-11-07 15:06:55
########################################################

import pyspeckit
sp = pyspeckit.Spectrum('sn2009ip_halpha.fits')
sp.data = 2-sp.data
sp.baseline()
sp.plotter(xmin=6300, xmax=6700)
sp.specfit(plot=True, fittype='voigt')
fwhm = sp.specfit.measure_approximate_fwhm(threshold='error', emission=False, interpolate_factor=1024, plot=True, grow_threshold=1)
