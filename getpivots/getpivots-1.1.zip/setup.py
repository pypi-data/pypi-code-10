from setuptools import setup

setup(
	name='getpivots',
	version = '1.1',
	url = 'https://github.com/nhsb1/pivot-point-calculator',
	scripts=['gp.py'],
	install_requires=['ystockquote', 'yahoo_finance','regex', 'argparse','datetime'])
 


