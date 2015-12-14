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
from solver import *
import numpy as np
from tst.tst_test import tst_matrix, ListComp, hypo_decorator, unittest
from scipy.linalg import cho_solve_banded

alpha = 2.
beta = -0.5
class TestSolver(ListComp):
	@hypo_decorator
	def test_cholesky_TST(self, b):
		c = cholesky_TST(alpha, beta, len(b))
		x = cho_solve_banded((c,False), b)

		b2 = np.dot(tst_matrix(alpha, beta, len(x)), x)

		self.assertListAlmostEqual(b, b2, 5)

	@hypo_decorator
	def test_cholesky_AApI(self, b):
		c = cholesky_AApI(alpha, beta, len(b))
		x = cho_solve_banded((c,False), b)

		A = tst_matrix(alpha, beta, len(b))
		AApI = np.dot(A, A) + np.eye(len(b))

		b2 = np.dot(AApI, x)

		self.assertListAlmostEqual(b, b2, 5)

	@hypo_decorator
	def test_crank_nicolson(self, b):
		s = Crank_Nicolson(1, 1, len(b))
		dt = s.longest_time_step()*abs(b[0])
		s.set_time_step(dt)
		b2 = s.advance(b)

		A = tst_matrix(1 + s.q, -s.q/2., len(b))
		B = tst_matrix(1 - s.q, s.q/2., len(b))

		y1 = np.dot(A, b2)
		y2 = np.dot(B, b)

		self.assertListAlmostEqual(y1, y2, 5)

	@hypo_decorator
	def test_schrodinger(self, s):
		br = np.array(s[0:len(s)/2*2:2])
		bj = np.array(s[1::2])

		s = Schrodinger(1, 1, len(br))
		dt = s.longest_time_step()*abs(br[0])
		s.set_time_step(dt)
		br2, bj2 = s.advance(br, bj)

		A = np.eye(len(br)) + 1j*tst_matrix(s.q, -s.q/2., len(br))
		B = np.eye(len(br)) - 1j*tst_matrix(s.q, -s.q/2., len(br))

		y1 = np.dot(A, br2+1j*bj2)
		y2 = np.dot(B, br+1j*bj)

		self.assertListAlmostEqual(y1, y2, 5)

if __name__=="__main__":
	unittest.main()
