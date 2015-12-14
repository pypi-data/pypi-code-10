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
import numpy as np

def integrate_source(data, i, f1, f2, dt):
	"""
	Function to integrate a source using the Trapezium rule
		u_t = f
	where f1 = f(t) and f2 = f(t+dt)
	"""
	data += (0.5*dt) * (f1+f2)
	return data

def evolve_potential(data, V, dt):
	"""
	Function to be combined with a solver to add a potential of the form:
		u_t = V * u
		so u^(n+1)/u^n = exp(V*dt)
	"""
	c = np.exp(V*dt)
	return data*c

def complex_multiply(xr, xj, yr, yj):
	"""
	Do complex multiplication when the data is given as real and imaginary
	parts separately
	"""
	return (xr*yr - xj*yj, xr*yj + xj*yr)

def evolve_complex_potential(dr, dj, V, dt):
	"""
	Function to be combined with a solver to add a potential of the form:
		i*u_t = V * u
		so u^(n+1)/u^n = exp(-i*V*dt)
	"""
	c = np.exp(-1j*V*dt)
	return complex_multiply(dr, dj, c.real, c.imag)
