try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'My Project',
	'author': 'Barbara Rodriguez',
	'url': 'URL to get it at.',
	'download_url': 'Where to download it.',
	'author_email': 'barbarajrodriguez542@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['RE_4'],
	'scripts': [],
	'name' : 'RE_4_stuff'
	}
	
setup(**config)