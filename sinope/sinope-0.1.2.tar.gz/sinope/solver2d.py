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
from solver import Crank_Nicolson, Schrodinger
import numpy as np

class Dimensionally_Split(object):
	"""
	An abstract class for using 1D solvers and dimensional splitting to
	construct 2D solvers
	"""
	def __init__(self, alpha, dx, nx, dy, ny):
		self.sx = self.base_solver()(alpha, dx, nx)
		self.sy = self.base_solver()(alpha, dy, ny)

	def base_solver(self):
		raise NotImplementedError

	def longest_time_step(self):
		# Use longest which satisfies restriction from each dimension
		return min(self.sx.longest_time_step(), self.sy.longest_time_step())

	def set_time_step(self, dt):
		self.sx.set_time_step(dt)
		self.sy.set_time_step(dt)

class Crank_Nicolson2D(Dimensionally_Split):
	"""
	A solver for 2D real diffusion equations using the Crank_Nicolson solver
	and dimensional splitting
	"""
	def base_solver(self): return Crank_Nicolson

	def advance(self, data):
		for row in xrange(np.shape(data)[0]):
			data[row] = self.sx.advance(data[row])

		for col in xrange(np.shape(data)[1]):
			data[:,col] = self.sy.advance(data[:,col])

		return data

class Schrodinger2D(Dimensionally_Split):
	"""
	A solver for 2D diffusion equations with imaginary diffusion
	coefficientusing the Schrodinger solver and dimensional splitting
	"""
	def base_solver(self): return Schrodinger

	def advance(self, dr, dj):
		for row in xrange(np.shape(dr)[0]):
			dr[row], dj[row] = self.sx.advance(dr[row], dj[row])

		for col in xrange(np.shape(dj)[1]):
			dr[:,col], dj[:,col] = self.sy.advance(dr[:,col], dj[:,col])

		return (dr, dj)
