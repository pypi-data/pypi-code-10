try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'A Resident Evil Game.',
	'author': 'Barbara Rodriguez',
	'url': 'https://pypi.python.org/pypi?%3Aaction=pkg_edit&name=RE_2',
	'download_url': 'https://pypi.python.org/pypi?%3Aaction=pkg_edit&name=RE_2',
	'author_email': 'barbarajrodriguez542@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['RE_2'],
	'scripts': ['bin/dist/config.exe', 'bin/dist/RE_2.exe', 'bin/dist/zombie_combat.exe', 'bin/dist/stats.exe'],
	'name' : 'Resident_Evil_stuff',
	}
	
setup(**config)