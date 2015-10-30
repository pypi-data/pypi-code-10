from setuptools import setup, find_packages

version = '1.5'

long_description = (
    open("README.rst").read() + "\n" + open("HISTORY.txt").read()
)

setup(name='Products.PTProfiler',
      version=version,
      description="PageTemplate profiler for Zope 2",
      long_description=long_description,
      classifiers=[
          "Framework :: Zope2",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='zope2 page template profiler',
      author='Guido Wesdorp and Infrae',
      author_email='info@infrae.com',
      url='https://github.com/infrae/Products.PTProfiler',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          ],
      extras_require=dict(
          test=[
              'plone.testing',
          ]),
      )
