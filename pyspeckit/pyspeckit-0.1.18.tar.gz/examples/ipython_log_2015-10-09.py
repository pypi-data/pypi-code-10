########################################################
# Started Logging At: 2015-10-09 09:15:55
########################################################

get_ipython().system(u'mvim -p ammonia_*')
get_ipython().magic(u'run ammonia_fit_example.py')
get_ipython().system(u'find .. -name "G031*"')
get_ipython().magic(u'cd pyspeckit/tests')
get_ipython().magic(u'cd ../pyspeckit/tests/')
get_ipython().magic(u'run ../../examples/ammonia_fit_example.py')
pl.draw(); pl.show()
sp.specfit(fittype='ammonia',
           guesses=[5.9,4.45,8.3e14,0.84,96.2,0.43],
           quiet=False, thin=True)
"%g" % 8.3e14
sp.specfit.fitter.annotations()
sp.specfit.fitter
sp.specfit.fitter.parinfo
sp.specfit.fitter.parinfo[2].value
"%g" % sp.specfit.fitter.parinfo[2].value
from decimal import Decimal # for formatting
Decimal("%g" % pinfo['value']).quantize(Decimal("%0.2g" % (min(pinfo['error'],pinfo['value']))))
pinfo = sp.specfit.parinfo
Decimal("%g" % pinfo['value']).quantize(Decimal("%0.2g" % (min(pinfo['error'],pinfo['value']))))
pinfo = sp.specfit.parinfo[2]
Decimal("%g" % pinfo['value']).quantize(Decimal("%0.2g" % (min(pinfo['error'],pinfo['value']))))
("%g" % pinfo['value']).quantize(Decimal("%0.2g" % (min(pinfo['error'],pinfo['value']))))
"%g" % (Decimal("%g" % pinfo['value']).quantize(Decimal("%0.2g" % (min(pinfo['error'],pinfo['value'])))))
