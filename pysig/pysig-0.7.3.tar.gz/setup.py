from distutils.core import setup
from sig import VERSION

setup(
  name = 'pysig',
  packages = ['sig','sig.utils','sig.carrier'],
  version = "%s" % (VERSION),
  description = 'pysig is a library intended to manage events dispatching locally or over a network',
  author = 'Alexandru Mircescu',
  author_email = 'mircescu@gmail.com',
  url = 'http://pysig.rtfd.org',
  download_url = 'https://bitbucket.org/madlex/pysig/get/package.tar.gz',
  keywords = ['event', 'signaling', 'messaging', 'network', 'dispatch'],
  license = "MIT",
  platforms = "any",
  classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ]
)
