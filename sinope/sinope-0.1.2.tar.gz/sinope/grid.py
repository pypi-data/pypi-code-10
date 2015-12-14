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
from utilities import Struct, check_regular_array_equality

class Grid(object):
	"""
	Grid class for controlling finite difference simulations

	The ith component is stored in self.data[i]

	Some methods need to be specified by the user. You should inherit from
	either Grid1D or Grid2D. Since these classes have save/load and initialise
	methods too
	"""
	def __init__(self, **kwargs):
		self.time = 0.0

		# A struct containing everything passed to the constructor
		self.param = Struct(**kwargs)

		self.initialise_data()
		self.initialise_solvers()

	def run(self, filename, t, rerun=False, quiet=False):
		"""
		Check if file already exists, if it does, load it and return it.
		Otherwise advance to the given time.

		If the resolution is changed or the target times are changed, the
		program will re-run intelligently as required.  However, if the initial
		conditions, potential etc are changed you might get a mixture of old
		and new data
		"""
		if not rerun:
			try:
				self.load(filename)
				self.time = t
			except (IOError, AssertionError):
				pass
			else:
				return # If data is loaded successfully, then we are done
		self.advance(t, quiet=quiet)
		self.save(filename)

	def advance(self, target, dt=None, quiet=False):
		"""
		Advance the solution to the target time

		If dt is None, then use the largest possible time step while ensuring
		that the solution does not overshoot the target time
		"""
		self.set_time_step(dt)

		while target - self.time >= self.dt:
			self.advance_single()
			self.time += self.dt

		if target - self.time > 1e-10:
			self.set_time_step(target - self.time)
			self.advance_single()
			self.time = target

		if not quiet: print "Advanced to %.2e" % self.time

	# --------------------------------------
	# Methods to be overwritten in Grid1D and Grid2D
	# --------------------------------------
	def initialise_data(self):
		raise NotImplementedError

	def save(self, filename):
		"""Save data to file"""
		raise NotImplementedError

	def load(self, filename):
		"""Load data from file created using save"""
		raise NotImplementedError

	def initialise(self, f, i=0):
		"""Initialise the ith component of the data using the function f"""
		raise NotImplementedError

	# --------------------------------------
	# Methods to be overwritten by the user
	# --------------------------------------
	def n_components(self):
		"""Number of components to be solved together (default is 1)."""
		return 1

	def initialise_solvers(self):
		"""
		Construct (and store as member data) whichever solvers are required.
		"""
		raise NotImplementedError

	def set_time_step(self, dt):
		"""
		Assign dt to self.dt

		If dt is None, this method should calculate the longest acceptable time
		step

		Any preparation of solvers (Cholesky factorisations) should be called
		from here
		"""
		raise NotImplementedError

	def advance_single(self):
		"""
		Advance each component of the solution by a single time step (self.dt)
		"""
		raise NotImplementedError

class Grid1D(Grid):
	"""
	Grid class for controlling finite difference simulations
	Specialised for 1D grids
	"""
	def initialise_data(self):
		self.x, self.dx = np.linspace(
				self.param.xmin, self.param.xmax, self.param.nx, retstep=True
			)
		# Remove boundary points
		self.x = self.x[1:-1]

		# Initialise numpy array for storing data
		self.data = np.zeros(
				(self.n_components(),len(self.x))
			)

	def save(self, filename):
		with open(filename+".npz", "w") as f:
			np.savez(f, x=self.x, data=self.data)

	def load(self, filename):
		f = np.load(filename+".npz")
		assert check_regular_array_equality(self.x, f["x"])
		self.data = f["data"]

	def initialise(self, f, i=0):
		self.data[i] = f(self.x)

class Grid2D(Grid):
	"""
	Grid class for controlling finite difference simulations
	Specialised for 2D grids
	"""
	def initialise_data(self, **kwargs):
		self.x, self.dx = np.linspace(
				self.param.xmin, self.param.xmax, self.param.nx, retstep=True
			)
		# Remove boundary points
		self.x = self.x[1:-1]

		self.y, self.dy = np.linspace(
				self.param.ymin, self.param.ymax, self.param.ny, retstep=True
			)
		# Remove boundary points
		self.y = self.y[1:-1]

		self.X, self.Y = np.meshgrid(self.x, self.y)

		# Initialise numpy array for storing data
		self.data = np.zeros(
				(self.n_components(),len(self.y),len(self.x))
			)

	def save(self, filename):
		with open(filename+".npz", "w") as f:
			np.savez(f, x=self.x, y=self.y, data=self.data)

	def load(self, filename):
		f = np.load(filename+".npz")
		c1 = check_regular_array_equality(self.x, f["x"])
		c2 = check_regular_array_equality(self.y, f["y"])
		assert c1 and c2
		self.data = f["data"]

	def initialise(self, f, i=0):
		self.data[i] = f(self.X, self.Y)
