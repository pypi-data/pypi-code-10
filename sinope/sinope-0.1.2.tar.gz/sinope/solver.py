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
from tst import *
from scipy.linalg import cholesky_banded, cho_solve_banded

def cholesky_TST(alpha, beta, n):
	"""
	Return the Cholesky factorisation of the matrix TST(alpha, beta).

 	If for example alpha=a, beta=b, n=5, then TST(alpha, beta) is:
 		(a b 0 0 0)
 		(b a b 0 0)
 		(0 b a b 0)
 		(0 0 b a b)
 		(0 0 0 b a)
	"""
	A = np.zeros((2,n))
	A[0,:] = beta
	A[1,:] = alpha

	return cholesky_banded(A)

def cholesky_AApI(alpha, beta, n):
	"""
	Return the Cholesky factorisation of the matrix:
		(AA + I) where A is TST(alpha, beta)

 	    (a b      )   (a b      )   (a2+b2+1   2ab       b2                   )
 	    (b a b    )   (b a b    )   (2ab       a2+2b2+1  2ab       b2         )
	I + (  b a b  ) * (  b a b  ) = (b2        2ab       a2+2b2+1  2ab      b2)
 	    (    b a b)   (    b a b)   (
 	    (      b a)   (      b a)   (
	"""
	AApI = np.zeros((3,n))
	AApI[0,:] = beta**2
	AApI[1,:] = 2*alpha*beta
	AApI[2,1:-1] = alpha**2 + 2*beta**2 + 1
	AApI[2,(0,-1)] = alpha**2 + beta**2 + 1

	return cholesky_banded(AApI)

class Explicit(object):
	"""
	Solver for the PDE:
	d_t u = alpha * d_xx u

	let mu = dt/dx**2
	let q = mu*alpha

	u^(n+1) = u^n + alpha*mu * (u_i+1 + u_i-1 - 2*u_i)
	        = (1-2q)*u_i + q*(u_i+1 + u_i-1)
	        = TST(1-2q, q) u^n

	For stability require:
		q < 0.5
	"""
	def __init__(self, alpha, dx):
		self.alpha = alpha
		self.dx = dx

	def longest_time_step(self):
		mu = 0.45/self.alpha
		return mu * self.dx**2

	def set_time_step(self, dt):
		self.q = self.alpha * dt / self.dx**2

	def advance(self, data):
		return TSTmultiply(1-2*self.q, self.q, data)

class Implicit(object):
	"""
	A parent class for implicit solvers with no stict stability condition
	"""
	def __init__(self, alpha, dx, nx):
		self.alpha = alpha
		self.dx = dx
		self.nx = nx

	def longest_time_step(self):
		return self.dx / self.alpha

class Crank_Nicolson(Implicit):
	"""
	Solver for the PDE:
	d_t u = alpha * d_xx u ; where alpha is real

	let mu = dt/dx**2
	let q = mu*alpha

	u^(n+1) - u^n = mu*alpha * (
		0.5 * (u_i+1 + u_i-1 - 2*u_i)^n+1 +
		0.5 * (u_i+1 + u_i-1 - 2*u_i)^n   +
		)

	TST(1+q, -q/2) u^(n+1) = TST(1-q, q/2) u^n

	No stability requirement, choose
		q = 1./dx = dt*alpha / dx**2
		so dt = dx/alpha
	"""
	def set_time_step(self, dt):
		self.q = self.alpha * dt / self.dx**2

		# Store the Cholesky factors in self.c
		self.c = cholesky_TST(1+self.q, -self.q/2., self.nx)

	def advance(self, data):
		data = TSTmultiply(1-self.q, self.q/2., data)
		return cho_solve_banded((self.c,False), data)

class Schrodinger(Implicit):
	"""
	Solver for the PDE:
	d_t u = alpha * i * d_xx u

	__init__ and longest_time_step are inherited from Crank_Nicolson

	let mu = dt/dx**2
	let q = mu*alpha

	u^(n+1) - u^n = mu*alpha*i * (
		0.5 * (u_i+1 + u_i-1 - 2*u_i)^n+1 +
		0.5 * (u_i+1 + u_i-1 - 2*u_i)^n   +
		)

	(I + iA) u^(n+1) = (I - iA) u^n ; where A = TST(q, -q/2)

	No stability requirement, choose
		q = 1./dx = dt*alpha / dx**2
		so dt = dx/alpha

	let u^(n+1) = x = (xr+1j*xj) (real and imag parts)
	let u^n     = b = (br+1j*bj)

	    x = (I+iA)^-1 (I-iA) b
	      = (I+iA)^-1 (2I - (I+iA)) b
	  x+b = (I+iA)^-1 2*b

	Let y = x+b = (yr+1j*yj). Separating real and imaginary parts yields
		y_r - Ay_j = 2*b_r
		Ay_r + y_j = 2*b_j

	For xr we have:
		(AA+I) y_r = 2 * (Ab_j + b_r)      <-- AApIy_r
		       x_r = y_r - b_r

	For xj:
		       y_j = 2*b_j - Ay_r
		       x_j = y_j - b_j
		           = b_j - A*y_r
	"""
	def set_time_step(self, dt):
		self.q = self.alpha * dt / self.dx**2

		self.c = cholesky_AApI(self.q, -self.q/2., self.nx)

	def advance(self, br, bj):
		# Calculate (AA + I) yr = 2A*bj + 2br ; A = TST(q, -q/2)
		AApIy_r = TSTmultiply_plus_coeff(2*self.q, -self.q, 2, bj, br)

		# Solve for yr using choleksy factorisation
		yr = cho_solve_banded((self.c,False), AApIy_r)

		# Calculate xj = -A*yr + bj
		xj = TSTmultiply_plus(-self.q, 0.5*self.q, yr, bj)

		# return (xr, xj), xr=yr-br
		return (yr-br, xj)
