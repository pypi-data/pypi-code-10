from setuptools import setup

setup(
	name='rtq',
	version = '1.02',
	scripts=['rtqinfo.py'],
	install_requires=['bs4', 'yahoo_finance', 'BeautifulSoup', 'argparse', 'urllib3'])
 


