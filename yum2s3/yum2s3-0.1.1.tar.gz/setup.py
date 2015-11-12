from setuptools import setup, find_packages

setup(
    name='yum2s3',
    version='0.1.1',
    description='Creates custom repositories in s3',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'Click', 'pyum'
    ],
    entry_points='''
[console_scripts]
yum2s3=yum2s3:run
    ''',
    author_email='drew.sonne@gmail.com',
    author='Drew J. Sonne',
    url='https://github.com/drewsonne/yum2s3'
)
