# Copyright (c) 2015, Simon D. Wilkinson
#
# This file is part of Sinope. (https://github.com/sw561/sinope)
#
# Sinope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sinope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sinope.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------
#
#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

setup(name="sinope",
	description="A library for implicitly solving parabolic PDEs",
	url="https://github.com/sw561/sinope",
	author="Simon Wilkinson",
	author_email="sw561@cam.ac.uk",
	version='0.1.2',
	packages=["sinope","tst"],
	ext_modules=[Extension('tst/_ctst', ['tst/ctst.i', 'tst/ctst.cpp'],
	             swig_opts=['-c++', '-classic'])],
	scripts=["sinope_run_tests.py"],
	license="GPL",
	keywords=["numerical","parabolic","implicit","differential"],
	classifiers=[
		"Programming Language :: Python",
		"Operating System :: OS Independent",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Topic :: Scientific/Engineering :: Mathematics",
		"Topic :: Scientific/Engineering :: Physics",
		"Development Status :: 2 - Pre-Alpha",
		],
	long_description=open("README.rst").read()
	)
