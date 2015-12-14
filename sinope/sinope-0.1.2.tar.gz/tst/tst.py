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
# The functions in this module are an interface to those defined in ctst.cpp
# The python module ctst is generated using SWIG www.swig.org and the file
# numpy.i from http://docs.scipy.org/doc/numpy-1.6.0/reference/swig.html

import numpy as np
import ctst

def py_TSTmultiply(alpha, beta, x):
	"""
	Calculate A*x where A is TST(alpha, beta)

	TST(alpha, beta) with alpha=a, beta=b, x of length 5:
		(a b 0 0 0)
		(b a b 0 0)
		(0 b a b 0)
		(0 0 b a b)
		(0 0 0 b a)
	"""
	y = alpha*x
	y[:-1] += beta*x[1:]
	y[1:] += beta*x[:-1]
	return y

def TSTmultiply(alpha, beta, x):
	"""Calculate A*x where A is TST(alpha, beta)"""
	interm = np.zeros(len(x))
	ctst.TSTmultiply(alpha, beta, x, interm)
	return interm

def TSTmultiply_plus(alpha, beta, x, b):
	"""Calculate A*x + b where A is TST(alpha, beta)"""
	interm = np.zeros(len(x))
	ctst.TSTmultiply_plus(alpha, beta, x, b, interm)
	return interm

def TSTmultiply_plus_coeff(alpha, beta, coeff, x, b):
	"""Calculate A*x + coeff*b where A is TST(alpha, beta)"""
	interm = np.zeros(len(x))
	ctst.TSTmultiply_plus_coeff(alpha, beta, coeff, x, b, interm)
	return interm
