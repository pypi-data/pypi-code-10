try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'A Resident Evil Game',
	'author': 'Barbara Rodriguez',
	'url': 'http://pypi.python.org/pypi/RE_1',
	'download_url': 'http://pypi.python.org/pypi/RE_1',
	'author_email': 'barbarajrodriguez542@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['RE_1'],
	'scripts': [],
	'name' : 'RE_1'
}
	
setup(**config)