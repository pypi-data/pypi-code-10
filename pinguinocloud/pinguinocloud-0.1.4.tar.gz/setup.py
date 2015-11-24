#!/usr/bin/env python


from setuptools import setup, find_packages


setup(name = "pinguinocloud",
      version = "0.1.4",
      description = "Open Hardware Electronics Prototyping Platform, Open Source Integrated Development Environment (IDE)",
      description_file = "README.rst",

      author = "",
      author_email = "",
      maintainer = "Yeison Cardona",
      maintainer_email = "yeison.eng@gmail.com",

      url = "http://www.pinguino.cc/",
      download_url = "",

      license = "GPLv2",
      install_requires = ["pyusb==1.0.0b2", "requests"],
      keywords = "microchip, electronic, prototyping, IDE",

      classifiers=[#list of classifiers in https://pypi.python.org/pypi?:action=list_classifiers
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
                   "Operating System :: POSIX :: Linux",
                   "Programming Language :: Python",
                   ],

      scripts = ["bin/pinguinohandler",
                 ],

      packages = find_packages(),

      include_package_data = True,

      data_files=[
          ("/usr/share/applications", ["pinguinohandler.desktop"]),
          ],

      zip_safe = False
      )