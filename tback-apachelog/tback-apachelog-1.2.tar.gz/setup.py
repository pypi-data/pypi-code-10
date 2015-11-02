from distutils.core import setup

# From inspecting Mark Pilgrims feedparser...
# patch distutils if it can't cope with the "classifiers" or "download_url"
# keywords (prior to python 2.3.0).
#
# A note to Harry:
# I'm not trying to steal your work. The project was archived on google.
# I wanted python3 compatibility. I changed what was necessary and pushed it
# to pypi under a new name. Feel free to contact me if you think I could have
# done better.
#
from distutils.dist import DistributionMetadata
if not hasattr(DistributionMetadata,'classifiers'):
    DistributionMetadata.classifiers = None
    
setup(
    name = 'tback-apachelog',
    version = '1.2',
    description = 'Access log parser in python, ported from '\
    'Peter Hickman\'s Apache::LogRegex Perl moduleUniversal.',
    long_description = """\
Apache Log Parser
-----------------

Parser for extracting fields from a single line of an Apache
access.log (should work for other servers conforming to the
Common Log Format).

Create the parser with the log format from your server .conf
file, parse lines to get dict corresponding to fields defined
in the log format.


""",
    author='Harry Fuecks',
    author_email = 'hfuecks@gmail.com',
    maintainer = 'Till Backhaus',
    maintainer_email = 'till@backha.us',
    url = 'https://github.com/tback/apachelog',
    license = "Artistic License / GPLv2",
    platforms = ['POSIX', 'Windows'],
    keywords = ['apache', 'log', 'parser'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Artistic License",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: Log Analysis",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        ],
    py_modules = ['apachelog',]
    )
