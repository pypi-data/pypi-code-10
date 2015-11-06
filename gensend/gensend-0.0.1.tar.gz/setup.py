from setuptools import setup, find_packages


setup(
    name='gensend',
    version='0.0.1',
    packages=find_packages(),
    entry_points={'console_scripts': [
        'gensend = gensend.cmd:execute_gensend',
    ]},
    package_data={'': ['*Makefile*']},
    include_package_data=True,
    install_requires=[
      'fake-factory>=0.5.2',
      'netaddr>=0.7.17',
    ],
    url='https://github.com/cstockton/gensend'
)
