#!/usr/bin/env python


from setuptools import setup, find_packages

setup(name = "python-openexchangerates",
      version = "0.1.0",
      packages = find_packages(),
      include_package_data=True,
      description = "Open exchange rates",
      description_file = "README.rst",

      author = "Yeison Cardona",
      author_email = "yeison.eng@gmail.com",
      maintainer = "Yeison Cardona",
      maintainer_email = "yeison.eng@gmail.com",

      url = "http://python-bitcoinopenexchange.readthedocs.org/en/latest/",
      download_url = "https://bitbucket.org/yeisoneng/python-openexchangerates/src",

      license = "BSD 3-Clause",
      install_requires = ["requests",],
      # keywords = '',

      classifiers=[#list of classifiers in https://pypi.python.org/pypi?:action=list_classifiers

                   ],
      )
