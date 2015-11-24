from setuptools import setup, find_packages

module_name = 'quaycon'
root_url = 'https://github.com/cogniteev/' + module_name

__version__ = None
with open('{}/__init__.py'.format(module_name)) as istr:
    for l in filter(lambda l: l.startswith('__version__ ='), istr):
        exec(l)
__version__ = '.'.join(map(str, __version__))

setup(
    name=module_name,
    version=__version__,
    description='Rebuild your Quay.io repositories when base image changes',
    author='Cogniteev',
    author_email='tech@cogniteev.com',
    url=root_url,
    download_url=root_url + '/tarball/' + __version__,
    license='Apache license version 2.0',
    keywords='cogniteev docido',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    packages=find_packages(exclude=['*.tests']),
    test_suite='docido.sdk.test.suite',
    zip_safe=True,
    install_requires=[
        'flask==0.10.1',
        'mongoengine>=0.10.0',
        'python-dateutil>=2.4.2',
        'pytz>=2015.6',
        'PyYAML>=3.11',
        'requests>=2.8.1',
        'six>=1.10.0',
    ],
    entry_points="""
        [console_scripts]
        quaycon = quaycon.cli:main
    """
)
