from setuptools import setup

def readme():
    with open('readme.rst') as f:
        return f.read()

setup(name='mpcouch',
    version='0.2.6-dev',
    description='A multiprocess bulk-uploading helper for CouchDB',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3.2',
        'Topic :: Database',
    ],
    keywords='couchdb multiprocessing upload bulk',
    url='https://github.com/scubbx/couch-bulk-multiprocess',
    author='Markus Mayr',
    author_email='markusmayr@gmx.net',
    license='MIT',
    packages=['mpcouch'],
    install_requires=[
        'couchdb',
    ],
    zip_safe=False)
