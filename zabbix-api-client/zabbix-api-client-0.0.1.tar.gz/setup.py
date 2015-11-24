from setuptools import setup

long_description = open('./README.rst').read()

setup(
    name="zabbix-api-client",
    version="0.0.1",
    install_requires=[
        'requests==2.8.1',
        'jsonschema>=2.5.1',
        'python-dateutil>=2.4.2'
    ],
    description='Zabbix API client library',
    long_description=long_description,
    url='https://github.com/osamunmun/zabbix-api-client',
    author='Osamu Takayasu',
    author_email='osamu.takayasu@gmail.com',
    license='MIT',
    packages=['zabbix_api_client']
)
