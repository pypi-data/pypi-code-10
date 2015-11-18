from setuptools import setup, find_packages

version = '0.0.1'

setup(name="helga-bugzilla",
      version=version,
      description=('bugzilla plugin for helga'),
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords='irc bot bugzilla',
      author='ken dreyer',
      author_email='ktdreyer [at] ktdreyer [dot] com',
      url='https://github.com/ktdreyer/helga-bugzilla',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'python-bugzilla',
      ],
      tests_require=[
          'python-bugzilla',
      ],
      entry_points = dict(
          helga_plugins = [
              'bugzilla = helga_bugzilla:helga_bugzilla',
          ],
      ),
)
