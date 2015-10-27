from setuptools import setup

setup(
	name='rtq',
	version = '1.04',
	scripts=['rtqinfo.py'],
	install_requires=['lxml','beautifulsoup4', 'yahoo_finance', 'BeautifulSoup', 'argparse', 'urllib3'])
 


