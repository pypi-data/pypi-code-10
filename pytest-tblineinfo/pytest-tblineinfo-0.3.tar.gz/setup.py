# Deactivate hard links that do not work in a mounted directory in a Docker
# container
import os
del os.link

from setuptools import setup
import codecs

setup(
    name="pytest-tblineinfo",
    version = "0.3",
    description = (
        'tblineinfo is a py.test plugin that insert the node id in the final '
        'py.test report when --tb=line option is used'
    ),
    long_description=codecs.open("README.rst", encoding='utf-8').read(),
    author = 'Mathieu Clabaut',
    author_email = 'mathieu.clabaut@systerel.fr, mathieu@clabaut.net',
    py_modules=['pytest_tblineinfo'],
    # the following makes a plugin available to pytest
    entry_points={'pytest11': ['tblineinfo = pytest_tblineinfo']},
    platforms='any',
    install_requires=[
                'pytest>=2.0',
            ],
    license='MIT',
    url='https://github.com/matclab/pytest-tblineinfo',
    classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Operating System :: POSIX',
                'Operating System :: Microsoft :: Windows',
                'Operating System :: MacOS :: MacOS X',
                'Topic :: Software Development :: Testing',
                'Topic :: Software Development :: Libraries',
                'Topic :: Utilities',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: Implementation :: PyPy',
            ]
)
