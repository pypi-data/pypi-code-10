from setuptools import setup, find_packages

setup(
	name='pyroclast',
	version='0.9.0',
	packages=find_packages(),
	install_requires=['xlrd>=0.9.4','unqlite>=0.4.1'],
	package_data={
		'': ['*.html','*.txt','*.md','*.json','*.csv','*.sql','*.unq','*.xlsx','*.xls','*.xml']
	},
	author='Brian Kirkpatrick',
	author_email='code@tythos.net',
	description='Basic Python-based data server for exposing flat table and object hierarchy files via REST-ful queries',
	license='MIT',
	keywords='rest server json csv sqlite unqlite excel xml',
	url='https://github.com/Tythos/pyroclast',
	test_suite='pyroclast.test.suite',
)
