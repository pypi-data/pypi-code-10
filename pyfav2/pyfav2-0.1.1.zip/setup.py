from setuptools import setup, find_packages

install_requires = [
    "beautifulsoup4>=4.3.2",
    "requests>=2.1.0",
    "tldextract>=1.7.1",
]

classifiers = """
Intended Audience :: Developers
Intended Audience :: Science/Research
Natural Language :: English
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
"""

long_description = "pyfav2 is a simple Python library that helps you get a \
    favicon for a supplied URL. \
    Favicons can be annoying to track down because they're commonly located \
    in a handful of different places. pyfav2 removes the annoyance by handling \
    the details for you -- you supply a URL and pyfav2 will give you the \
    favicon."

setup( 
    name = 'pyfav2',
    version = '0.1.1',
    url = 'http://github.com/phillipsm/pyfav',
    author = 'Ashish Gupta',
    author_email = 'gupta.ashish65901@gmail.com',
    license = 'http://opensource.org/licenses/MIT',
    packages = find_packages(),
    install_requires = install_requires,
    description = 'You supply the URL, pyfav2 will supply the favicon',
    long_description=open('README.rst').read(),
    classifiers = filter(None, classifiers.split('\n')),
    keywords = ['favicon', 'favicons'],
    test_suite = 'test',
)