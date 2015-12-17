import os
from setuptools import setup

# confutil
# Configuration utility to ease navigation of local and system configurations

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "confutil",
    version = "0.1.1",
    description = "Configuration utility to ease navigation of local and system configurations",
    author = "Johan Nestaas",
    author_email = "johannestaas@gmail.com",
    license = "GPLv3+",
    keywords = "",
    url = "https://bitbucket.org/johannestaas/confutil",
    packages=['confutil'],
    package_dir={'confutil': 'confutil'},
    long_description=read('README.rst'),
    classifiers=[
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'configobj'
    ],
    entry_points = {
        'console_scripts': [
            'confutil = confutil:main',
        ],
    },
    #package_data = {
        #'confutil': ['catalog/*.edb'],
    #},
    #include_package_data = True,
)
