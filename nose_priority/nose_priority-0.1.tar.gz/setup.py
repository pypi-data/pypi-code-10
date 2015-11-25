from setuptools import setup

setup(name='nose_priority',
		version='0.1',
		description='Prioritize nose tests based on past failures',
		url='https://github.com/criles25/nose_priority',
		author='Charles Riley',
		author_email='criles25@gmail.com',
		license='GNU',
		packages=['nose_priority'],
		scripts=['bin/prioritize'],
		include_package_data=True,
		install_requires=['nose'],
		zip_safe=False)
