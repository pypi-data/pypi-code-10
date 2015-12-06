from __future__ import with_statement
from setuptools import setup, find_packages
import sys

version_classifiers = [
    'Programming Language :: Python :: %s' % version
    for version in [
        '2', '2.5', '2.6', '2.7',
        '3', '3.2', '3.3', '3.4', '3.5',
    ]]
other_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: BSD License',
    'Intended Audience :: Developers',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Testing',
    ]

with open('README', 'rt') as file_obj:
    detailed_description = file_obj.read()
with open('CHANGELOG', 'rt') as file_obj:
    detailed_description += file_obj.read()

install_requires = []
if (sys.version_info[0] == 2 and sys.version_info[1] < 7
    or sys.version_info[0] == 3 and sys.version_info[1] < 2):
    install_requires.append('argparse')

setup(
    name="nosy",
    version="1.2",
    description="""\
Run a specified command (by default, the nose test discovery and
execution tool) whenever a source file is changed.
    """,
    long_description=detailed_description,
    author="Doug Latornell",
    author_email="djl@douglatornell.ca",
    url="http://douglatornell.ca/software/python/Nosy/",
    license="New BSD License",
    classifiers=version_classifiers + other_classifiers,
    install_requires=install_requires,
    packages=find_packages(),
    entry_points={'console_scripts': ['nosy = nosy.nosy:main']}
)
