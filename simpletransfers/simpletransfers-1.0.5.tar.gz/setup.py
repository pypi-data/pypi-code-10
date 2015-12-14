from distutils.core import setup

setup(
	name = 'simpletransfers',
	version = '1.0.5',
	description = 'Simple file transfer library',
	author = 'Jesters Ghost',
	author_email = 'jestersghost@gmail.com',
	url = 'https://bitbucket.org/jestersghost/simpletransfers',
	requires = [ 'ctxlogger', 'Flask', 'paramiko', 'requests', 'suds' ],
	package_dir = { 'simpletransfers': '.' },
	packages = [
		'simpletransfers',
		'simpletransfers.tests',
	],
)
