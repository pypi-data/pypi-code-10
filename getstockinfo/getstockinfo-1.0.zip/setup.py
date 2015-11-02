from setuptools import setup

setup(
	name='getstockinfo',
	version = '1.0',
	url = 'https://github.com/nhsb1/getstockinfo',
	scripts=['getstockinfo-release.py'],
	install_requires=['yahoo_finance', 'argparse','datetime'])
 
	
