#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


if os.name == "posix": #GNU/Linux

    os_kwargs = {"data_files": [
                                ("/usr/share/applications", ["pinguino12.desktop"]),
                                ("/usr/share/icons/hicolor/256x256", ["pinguino/qtgui/resources/art/pinguino_logo-256x256.png"]),
                                ("/usr/share/icons/hicolor/256x256", ["pinguino/qtgui/resources/art/pinguino_logo_background_blue-256x256.png"]),
                                ],
                }

elif os.name == "os2":  #Mac OS X
    os_kwargs = {}


elif os.name == "nt":  #Windows
    os_kwargs = {}






setup(name = "pinguino",
      version = "12.0.15",
      description = "Open Hardware Electronics Prototyping Platform, Open Source Integrated Development Environment (IDE)",
      description_file = "README.rst",

      author = "",
      author_email = "",
      maintainer = "Yeison Cardona",
      maintainer_email = "yeison.eng@gmail.com",

      url = "http://www.pinguino.cc/",
      download_url = "",

      license = "GPLv2",
      keywords = "microchip, electronic, prototyping, IDE",

      classifiers=[#list of classifiers in https://pypi.python.org/pypi?:action=list_classifiers
                   "Environment :: X11 Applications :: Qt",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
                   "Operating System :: POSIX :: Linux",
                   "Programming Language :: Python",
                   ],

      packages = find_packages(),
      include_package_data = True,

      install_requires = [
                          "gitpython",
                          "hgapi",
                          "pyusb==1.0.0b2",
                          "pyside",
                          ],

      scripts = [
                 "bin/pinguino",
                 "bin/pinguino.pyw",
                 "bin/pinguino-cmd",
                 "bin/pinguino-cmd.py",
                 "bin/pinguino-reset",
                 "bin/pinguino-reset.py",
                 ],

      zip_safe = False,
      **os_kwargs

      )
