from setuptools import setup

setup(
    name='portcheck',
    version='0.3.0',
    author='J. Random Hacker',
    author_email='jrh@example.com',
    packages=['portcheck'],
	entry_points = {
			'console_scripts' : ['portcheck = portcheck.portcheck:main']
		},




)