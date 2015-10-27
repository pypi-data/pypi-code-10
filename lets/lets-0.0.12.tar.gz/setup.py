# -*- coding: utf-8 -*-
"""
Lets
~~~~

Utilities for gevent_ 1.0.

.. _gevent: http://gevent.org/

There're several ``gevent.Greenlet`` subclasses:

* ``Processlet`` -- maximizing multi-core use in gevent environment.
* ``Transparentlet`` -- keeping exc_info rather than printing exception.

And etc.:

* ``ObjectPool`` -- pooling objects. (e.g. connection pool)

See the next examples.

Examples
========

Processlet for bcrypt
---------------------

bcrypt_ is a library to hash password.  That the hashing is very heavy
CPU-bound task.  You can't guarantee concurrency with only gevent.  Use
``Processlet`` instead:

.. _bcrypt: https://github.com/pyca/bcrypt/

.. sourcecode:: python

   import bcrypt
   import gevent
   from lets import Processlet

   # bcrypt.hashpw is very heavy cpu-bound task.  it can spend a few seconds.
   def hash_password(password, salt=bcrypt.gensalt()):
       return bcrypt.hashpw(str(password), salt)

   def tictoc(delay=0.1):
       while True:
           print '.'
           gevent.sleep(delay)

   passwords = ['alfa', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot',
                'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike',
                'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra',
                'tango', 'uniform', 'victor', 'whiskey', 'xray', 'yankee',
                'zulu']

   # start tictoc
   gevent.spawn(tictoc)

   # Greenlet, tictoc pauses for a few seconds
   greenlet = gevent.spawn(hash_password, passwords[0])
   password_hash_0 = greenlet.get()

   # Processlet, tictoc never pauses
   processlet_1 = Processlet.spawn(hash_password, passwords[1])
   processlet_2 = Processlet.spawn(hash_password, passwords[2])
   password_hash_1 = processlet_1.get()
   password_hash_2 = processlet_2.get()

You can also limit the number of child processes with ``ProcessPool``:

.. sourcecode:: python

   import multiprocessing
   from lets import ProcessPool

   pool_size = max(multiprocessing.cpu_count() - 1, 1)
   pool = ProcessPool(pool_size)
   password_hashes = pool.map(hash_password, passwords)

Memcached connection pool
-------------------------

Greenlet-safe connection pool can be easily implemented by ``ObjectPool``:

.. sourcecode:: python

   import memcache
   from lets import ObjectPool

   mc_pool = ObjectPool(10, memcache.Client, [('localhost', 11211)])

   def save(key, val):
       with mc_pool.reserve() as mc:
           mc.set(key, val)

   for x, password_hash in enumerate(password_hashes):
       gevent.spawn(save, 'password_hashes[%d]' % x, password_hash)

   gevent.wait()

Links
=====

* `GitHub repository <http://github.com/sublee/lets>`_
* `development version
  <http://github.com/sublee/lets/zipball/master#egg=lets-dev>`_

"""
from __future__ import with_statement

import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


# prevent an error in atexit._run_exitfuncs.
__import__('multiprocessing')


# detect the current version.
with open('lets/__init__.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version


# use pytest instead.
class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='lets',
    version=version,
    license='BSD',
    author='Heungsub Lee',
    author_email=re.sub('((sub).)(.*)', r'\2@\1.\3', 'sublee'),
    url='https://github.com/sublee/lets',
    description='Several greenlet subclasses',
    long_description=__doc__,
    platforms='any',
    packages=['lets'],
    zip_safe=False,  # i don't like egg.
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Topic :: Software Development'],
    install_requires=['gevent', 'gipc'],
    tests_require=['psutil', 'pytest', 'pytest-rerunfailures'],
    cmdclass={'test': PyTest},
)
