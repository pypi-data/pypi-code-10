#!usr/bin/env python
"""planfftw provides FFT function planners corresponding to and expanding on
the variations provided by numpy.fft. Function planners for a number of FFT-
based operations are also provided, roughly corresponding to and expanding on
their scipy.signal counterparts.

PyFFTW is highly recommended, but not required. If it is not available,
planfftw will fall back on scipy.fftpack and/or numpy.fft."""

from .planners import (fft, 
                       rfft, 
                       fftn,
                       rfftn,
                       ifft,
                       irfft,
                       ifftn,
                       irfftn,
                       firfilter,
                       correlate,
                       convolve)

# clean up namespace
del planners

__version__ = '0.2'
