from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name = 'webs',
    version = '0.0.3',
    description = 'Web Scraping Tools',
    long_description = open(os.path.join(ROOT, 'README.rst')).read(),
    url = 'http://github.com/lorien/webs',
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',

    packages = find_packages(),
    include_package_data = True,
    scripts = ('bin/rps',),

    license = "MIT",
    keywords = "script web scraping console",
    classifiers = (
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ),
)
