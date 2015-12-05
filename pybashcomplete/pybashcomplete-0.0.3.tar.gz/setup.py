import os
import sys
from setuptools import setup

# pybashcomplete
# Bash completion utility for python scripts


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "pybashcomplete",
    version = "0.0.3",
    description = "Bash completion utility for python scripts",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://www.bitbucket.org/johannestaas/pybashcomplete",
    packages=['pybashcomplete'],
    package_dir={'pybashcomplete': 'pybashcomplete'},
    long_description=read('README.rst'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        #'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        #'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points = {
        'console_scripts': [
            'pybashcomplete = pybashcomplete:main',
            'pybashcomplete-install = pybashcomplete.config:main',
        ],
    },
    #package_data = {
        #'pybashcomplete': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)

