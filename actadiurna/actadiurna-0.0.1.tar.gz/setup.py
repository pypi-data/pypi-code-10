# Haze
#
# Author: Joe Block <jpb@unixorn.net>
# License: Apache 2.0

from setuptools import setup, find_packages

name = "actadiurna"
requirements = map(str.strip, open("requirements.txt").readlines())

setup(
  name = name,
  version = "0.0.1",
  description = "Acta Diurna is a tool for updating /etc/motd",
  author = "Joe Block",
  author_email = "jpb@unixorn.net",
  url = "https://github.com/unixorn/acta-diurna",
  download_url = "https://github.com/unixorn/acta-diurna/tarball/0.0.1",
  packages = find_packages(),
  install_requires = requirements,
  entry_points = {
    "console_scripts": [
      "acta-diurna = %s.cli:actaMain" % name
    ]
  }
)
