from distutils.core import setup


setup(
    name='migrations4neo',
    packages=['migrations4neo'],
    version='0.1',
    description='Easy neo4j migrations',
    author='turkus',
    author_email='wojciechrola@wp.pl',
    url='https://github.com/turkus/migrations4neo',
    download_url='https://github.com/turkus/migrations4neo/tarball/0.1',
    keywords=['neo4j', 'migrations'],
    entry_points={
        'console_scripts': [
            'mig4neo = migrations4neo.main:main',
        ]
    },
    install_requires=['py2neo', 'awesome-slugify'],
    classifiers=[],
)
