from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pyfun',
      version='0.1.4',
      description='The pyfun joke in the world',
      long_description='Really, the pyfun around.',
      classifiers=[
                        'Development Status :: 3 - Alpha',
                        'License :: OSI Approved :: MIT License',
                        'Programming Language :: Python :: 2.7',
                        'Topic :: Text Processing :: Linguistic',
                  ],
      test_suite='nose.collector',
      tests_require=['nose'],
      keywords='pyfun joke comedy flying circus',
      url='https://github.com/zhaohangbo/pyfun.git',
      author='zhaohangbo',
      author_email='zhaohangbo@example.com',
      license='MIT',
      packages=['pyfun'],

      #Command Line Interface: Way 1 bin/scripts
      scripts=['bin/pyfun-joke-bin-scripts',],
      #Command Line Interface: Way 2 entry_points
      entry_points = {
               'console_scripts': ['pyfun-joke-entry-points=pyfun.command_line:main'],
                     },

      #Imported Requirements
      install_requires=[
          'markdown',
#          packages can not found on pip          
#          dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0'],
          ],

#In order for Non-Code Files in MANIFEST.in to be copied at install time to the package's folder inside site-packages
      include_package_data=True,
      zip_safe=False)
