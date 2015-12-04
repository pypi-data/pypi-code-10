#!/usr/bin/env python
from elasticsearchcloudwatch import VERSION
import os.path
from glob import glob

from setuptools import find_packages, setup

def readme():
	path = os.path.join(os.path.dirname(__file__), 'README.md')
	if os.path.exists(path):
		with open(path) as f:
			return f.read()

setup(name='elasticsearchcloudwatch',
	version=VERSION,
	description='Elasticsearch monitoring scripts for CloudWatch',
	long_description=readme(),
	url='https://rubelw@bitbucket.org/rubelw/elasticsearchcloudwatch.git',
	author='Will Rubel',
	author_email='willrubel@gmail.com',
	license='Apache License (2.0)',
	keywords="elasticsearch monitoring cloudwatch amazon web services aws ec2",
	zip_safe=True,
	packages=find_packages(),
	install_requires=['boto>=2.33.0', 'elasticsearch>=2.1.0','prettyprint>=0.1.5','configparser>=2.4.0','boto3>=1.2.2'],
	entry_points={'console_scripts': [
		'get_web_request.py=elasticsearchcloudwatch.cli.get_web_request:main',
		'put_web_request.py=elasticsearchcloudwatch.cli.put_web_request:main',
		]
	},
	classifiers=[
		'License :: OSI Approved :: Apache Software License',
		'Topic :: System :: Monitoring'
	],
	data_files =    [
						('/etc/elasticsearchcloudwatch', ['config/example.config']),
					    ('/etc/elasticsearchcloudwatch', ['config/escw.config']),


					 ]

)
