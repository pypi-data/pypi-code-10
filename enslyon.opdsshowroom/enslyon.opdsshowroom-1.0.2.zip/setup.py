from setuptools import setup, find_packages
import os

version = '1.0.2'

setup(name='enslyon.opdsshowroom',
      version=version,
      description="Showroom for OPDS Feed",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        ],
      keywords='Plone plone rest REST OPDS opds',
      author='Encolpe DEGOUTE',
      author_email='encolpe@colpi.org',
      url='https://github.com/collective/enslyon.opdsshowroom',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['enslyon'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'plone.api',
          'setuptools',
          'plone.app.dexterity',
          # -*- Extra requirements: -*-
          'requests',
          'lxml',
          #'lineage.themeselection',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.app.contenttypes',
              'plone.app.robotframework[debug]',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
