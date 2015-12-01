import os
from setuptools import setup, find_packages

version = '0.1.1'

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst')) as fp:
    longdesc = fp.read()

try:
    with open(os.path.join(here, 'CHANGELOG.rst')) as fp:
        longdesc += "\n\n" + fp.read()
except OSError:
    pass


install_requires = [
    'click',
    'pyyaml',
]

entry_points = {
    'console_scripts': [
        'aliasfile = aliasfile.cli:main',
        ]
    }


setup(
    name='aliasfile',
    version=version,
    packages=find_packages(),
    url='https://github.com/rshk/aliasfile',
    license='BSD License',
    author='Samuele Santi',
    author_email='',
    description='',
    long_description=longdesc,
    install_requires=install_requires,
    entry_points=entry_points,
    # tests_require=tests_require,
    # test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',

        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',

        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    package_data={'': ['README.rst', 'CHANGELOG.rst']},
    include_package_data=True,
    zip_safe=False)
