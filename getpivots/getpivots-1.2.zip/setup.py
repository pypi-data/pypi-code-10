from setuptools import setup

setup(
	name='getpivots',
	version = '1.2',
	url = 'https://github.com/nhsb1/pivot-point-calculator',
	scripts=['getpivots.py'],
	install_requires=['ystockquote', 'yahoo_finance','regex', 'argparse','datetime'])
 


