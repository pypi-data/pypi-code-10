import os.path as osp
import re
from setuptools import setup, find_packages

import serenytics


RE_REQUIREMENT = re.compile(r'^\s*-r\s*(?P<filename>.*)$')


def pip(filename):
    requirements = []
    this_directory = osp.dirname(osp.abspath(__file__))
    for line in open(osp.join(this_directory, filename)).readlines():
        match = RE_REQUIREMENT.match(line)
        if match:
            requirements.extend(pip(match.group('filename')))
        else:
            requirements.append(line)
    return requirements


setup(
    name='serenytics',
    version=serenytics.__version__,
    description='Serenytics API client for python',
    install_requires=pip('requirements-serenytics.txt'),
    packages=find_packages(),
    include_package_data=True,
    author='Serenytics Team',
    author_email='support@serenytics.com',
    url='https://github.com/serenytics/docker-python-scripts',
    keywords=['serenytics', 'backend', 'hosted', 'cloud',
              'bi', 'dashboard', 'scripts', 'etl'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
