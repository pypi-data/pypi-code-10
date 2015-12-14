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
import os
import numpy as np

class Struct(object):
	"""
	A convenient class for packaging various variables into a "struct"
	It can be used like:

	>>> x = Struct(foo=1, bar=2)
	>>> print x.foo
	1
	>>> print x.bar
	2
	>>> x.baz = 3
	>>> print x.baz
	3
	"""
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

def ensure_dir(f):
	if not os.path.exists(f):
		os.makedirs(f)

def almost_equal(x, y):
	"""
	>>> almost_equal(0.1,0.100001)
	True
	>>> almost_equal(1e10,1e10+1)
	True
	>>> almost_equal(-0.001,0.001)
	False
	>>> almost_equal(0.01,0.02)
	False
	"""
	if abs(x-y)<=1e-5*max(abs(x), abs(y)): return True
	return False

def check_regular_array_equality(a, b):
	"""
	Check regular arrays are equal

	This function assumes the input arrays are both 'regular'. A regular array
	is one where the increment is constant, for example the arrays returned by
	numpy linspace

	>>> x = np.linspace(0,10,11)
	>>> y = np.linspace(0,10,11)
	>>> print check_regular_array_equality(x, y)
	True
	>>> y = np.linspace(0,10,12)
	>>> print check_regular_array_equality(x, y)
	False
	>>> y = np.linspace(0,11,11)
	>>> print check_regular_array_equality(x, y)
	False
	"""
	if len(a)!=len(b): return False
	if not almost_equal(a[0], b[0]): return False
	if not almost_equal(a[-1], b[-1]): return False
	if not almost_equal(a[1]-a[0], b[1]-b[0]): return False

	return True

if __name__=="__main__":
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	if failures==0: print "OK"
