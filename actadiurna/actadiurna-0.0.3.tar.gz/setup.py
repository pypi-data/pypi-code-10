# Haze
#
# Author: Joe Block <jpb@unixorn.net>
# License: Apache 2.0

from setuptools import setup, find_packages

name = "actadiurna"

setup(
  name = name,
  version = "0.0.3",
  description = "Acta Diurna is a tool for updating /etc/motd",
  author = "Joe Block",
  author_email = "jpb@unixorn.net",
  url = "https://github.com/unixorn/acta-diurna",
  download_url = "https://github.com/unixorn/acta-diurna/tarball/0.0.3",
  packages = find_packages(),
  entry_points = {
    "console_scripts": [
      "acta-diurna = %s.cli:actaMain" % name
    ]
  }
)
