# -*- coding: utf-8 -*-
__author__ = 'xuanwo'

from setuptools import setup, find_packages
import chineseregion

entry_points = {
    "console_scripts": [
        "chineseregion = chineseregion.main:main",
    ]
}

# with open("requirements.txt") as f:
#     requires = [l for l in f.read().splitlines() if l]

setup(
    name="chineseregion",
    version=chineseregion.__version__,
    description="a chinese region lib for python",
    author="xuanwo",
    author_email="xuanwo.cn@gmail.com",
    keywords="chinese, region, lib",
    license="MIT License",
    packages=find_packages(),
    entry_points=entry_points,
    # install_requires=requires,
    include_package_data=True,
    package_data={
        '': ['*.json']
    },
    classifiers=[
        'Development Status :: 3 - Alpha ',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
