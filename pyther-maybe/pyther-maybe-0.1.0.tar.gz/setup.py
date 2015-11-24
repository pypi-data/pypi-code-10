from setuptools import setup

import pyther_maybe
setup (
	name        = 'pyther-maybe'  ,
	version     = pyther_maybe.__version__         ,
	description = 'implementation of Maybe and Either data structures as python objects' ,
	license     = 'LGPLv3'         ,
	packages    = ['pyther_maybe'] ,
	)
