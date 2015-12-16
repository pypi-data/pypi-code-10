from setuptools import setup, find_packages
from codedeploy_monitor import __version__

# (c) Head In Cloud BVBA, Belgium
# http://www.headincloud.be


entrypoints = {
        'console_scripts': [
            'codedeploy_monitor = codedeploy_monitor.main_app:main',
        ],

}

name = "codedeploy_monitor"
author = "Jeroen Jacobs"
author_email = "info@headincloud.be"
description = "Creates and monitors AWS CodeDeploy deployments."
license = "GPLv3"
url = "http://github.com/headincloud/codedeploy_monitor"


def readme():
    with open('README.rst') as f:
        return f.read()

keywords = [
        "aws",
        "codedeploy",
]

requires = [
        'boto3>=1.2.0',
]

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX :: Linux',
    'Operating System :: MacOS :: MacOS X',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Topic :: System :: Software Distribution',
    ]


def main():
    setup(
        name=name,
        version=__version__,
        entry_points=entrypoints,
        packages=find_packages(),
        classifiers=classifiers,
        install_requires=requires,
        author=author,
        author_email=author_email,
        description=description,
        long_description=readme(),
        license=license,
        keywords=keywords,
        url=url,
    )


if __name__ == '__main__':
    main()
