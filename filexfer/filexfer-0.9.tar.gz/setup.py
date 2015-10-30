from distutils.core import setup

setup(name='filexfer',
      version='0.9',
      py_modules=['filexfer'],
      
      author='Wim Lewis', author_email='wiml@omnigroup com',
      url='http://pypi.python.org/pypi/filexfer',
      description="An implementation of the 'filexfer' protocol used by sftp.",
      long_description=
'''filexfer
========

The ``sftp`` program uses a protocol called `filexfer`_ to
communicate with the remote system. This Python module
implements filexfer, which allows you to drive an sftp
session safely without worrying about your local shell and
so on.

.. _filexfer: http://tools.ietf.org/html/draft-ietf-secsh-filexfer-13''',
      keywords=['sftp', 'ssh'],
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      license='BSD',
      )

