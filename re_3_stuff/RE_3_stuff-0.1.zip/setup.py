try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'My Project',
	'author': 'Barbara Rodriguez',
	'url': 'URL to get it at.',
	'download_url': 'Where to download it.',
	'author_email': 'barbararodriguez542@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['RE_3'],
	'scripts': ['bin/config.py', 'bin/stats.py', 'bin/zombie_combat.py', 'bin/RE_3_file.py'],
	'name' : 'RE_3_stuff'
	}
	
setup(**config)