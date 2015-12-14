from distutils.core import setup

setup(
	name = 'ctxlogger',
	version = '1.0.1',
	description = 'Add a context stack to log messages',
	author = 'Jesters Ghost',
	author_email = 'jestersghost@gmail.com',
	url = 'https://bitbucket.org/jestersghost/ctxlogger',
	package_dir = { 'ctxlogger': '.' },
	packages = [
		'ctxlogger',
	],
)
