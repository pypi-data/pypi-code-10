import numpy as np
import pyspeckit

xarr = np.linspace(-5,5,500)
sp = pyspeckit.Spectrum(xarr=xarr, data=xarr*0)
sigma = 1.0
taus = np.logspace(-1,3.2,100)

widths = []

for tau in taus:
    data = (1-np.exp(-tau*np.exp(-xarr**2/(sigma**2*2))))
    sp.data = data
    sp.error = data+1.0
    sp.specfit(fittype='gaussian', guesses=[1, 0, 1])
    widths.append(sp.specfit.parinfo['WIDTH0'])

import pylab as pl
w = [x.value for x in widths]
pl.figure(20).clf()
pl.plot(taus, w)
pars = np.polyfit(w, taus, 9)
pl.plot(np.polyval(pars, w), w, )


def tau_of_widthratio(x):
    return np.polyval(pars, x)

e2tau = [100, 77, 43]
ratio = [14.5/5.7, 10.9/5.7, 11.6/5.7]
pl.plot(e2tau, ratio, 's')
