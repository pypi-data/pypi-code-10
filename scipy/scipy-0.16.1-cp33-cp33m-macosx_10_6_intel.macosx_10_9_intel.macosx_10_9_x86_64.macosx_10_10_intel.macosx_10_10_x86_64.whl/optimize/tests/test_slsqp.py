"""
Unit test for SLSQP optimization.
"""
from __future__ import division, print_function, absolute_import

from numpy.testing import (assert_, assert_array_almost_equal, TestCase,
                           assert_allclose, assert_equal, run_module_suite)
import numpy as np

from scipy.optimize import fmin_slsqp, minimize


class MyCallBack(object):
    """pass a custom callback function

    This makes sure it's being used.
    """
    def __init__(self):
        self.been_called = False
        self.ncalls = 0

    def __call__(self, x):
        self.been_called = True
        self.ncalls += 1


class TestSLSQP(TestCase):
    """
    Test SLSQP algorithm using Example 14.4 from Numerical Methods for
    Engineers by Steven Chapra and Raymond Canale.
    This example maximizes the function f(x) = 2*x*y + 2*x - x**2 - 2*y**2,
    which has a maximum at x=2, y=1.
    """
    def setUp(self):
        self.opts = {'disp': False}

    def fun(self, d, sign=1.0):
        """
        Arguments:
        d     - A list of two elements, where d[0] represents x and d[1] represents y
                 in the following equation.
        sign - A multiplier for f.  Since we want to optimize it, and the scipy
               optimizers can only minimize functions, we need to multiply it by
               -1 to achieve the desired solution
        Returns:
        2*x*y + 2*x - x**2 - 2*y**2

        """
        x = d[0]
        y = d[1]
        return sign*(2*x*y + 2*x - x**2 - 2*y**2)

    def jac(self, d, sign=1.0):
        """
        This is the derivative of fun, returning a numpy array
        representing df/dx and df/dy.

        """
        x = d[0]
        y = d[1]
        dfdx = sign*(-2*x + 2*y + 2)
        dfdy = sign*(2*x - 4*y)
        return np.array([dfdx, dfdy], float)

    def fun_and_jac(self, d, sign=1.0):
        return self.fun(d, sign), self.jac(d, sign)

    def f_eqcon(self, x, sign=1.0):
        """ Equality constraint """
        return np.array([x[0] - x[1]])

    def fprime_eqcon(self, x, sign=1.0):
        """ Equality constraint, derivative """
        return np.array([[1, -1]])

    def f_eqcon_scalar(self, x, sign=1.0):
        """ Scalar equality constraint """
        return self.f_eqcon(x, sign)[0]

    def fprime_eqcon_scalar(self, x, sign=1.0):
        """ Scalar equality constraint, derivative """
        return self.fprime_eqcon(x, sign)[0].tolist()

    def f_ieqcon(self, x, sign=1.0):
        """ Inequality constraint """
        return np.array([x[0] - x[1] - 1.0])

    def fprime_ieqcon(self, x, sign=1.0):
        """ Inequality constraint, derivative """
        return np.array([[1, -1]])

    def f_ieqcon2(self, x):
        """ Vector inequality constraint """
        return np.asarray(x)

    def fprime_ieqcon2(self, x):
        """ Vector inequality constraint, derivative """
        return np.identity(x.shape[0])

    # minimize
    def test_minimize_unbounded_approximated(self):
        # Minimize, method='SLSQP': unbounded, approximated jacobian.
        res = minimize(self.fun, [-1.0, 1.0], args=(-1.0, ),
                       method='SLSQP', options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [2, 1])

    def test_minimize_unbounded_given(self):
        # Minimize, method='SLSQP': unbounded, given jacobian.
        res = minimize(self.fun, [-1.0, 1.0], args=(-1.0, ),
                       jac=self.jac, method='SLSQP', options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [2, 1])

    def test_minimize_bounded_approximated(self):
        # Minimize, method='SLSQP': bounded, approximated jacobian.
        with np.errstate(invalid='ignore'):
            res = minimize(self.fun, [-1.0, 1.0], args=(-1.0, ),
                           bounds=((2.5, None), (None, 0.5)),
                           method='SLSQP', options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [2.5, 0.5])
        assert_(2.5 <= res.x[0])
        assert_(res.x[1] <= 0.5)

    def test_minimize_unbounded_combined(self):
        # Minimize, method='SLSQP': unbounded, combined function and jacobian.
        res = minimize(self.fun_and_jac, [-1.0, 1.0], args=(-1.0, ),
                       jac=True, method='SLSQP', options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [2, 1])

    def test_minimize_equality_approximated(self):
        # Minimize with method='SLSQP': equality constraint, approx. jacobian.
        res = minimize(self.fun, [-1.0, 1.0], args=(-1.0, ),
                       constraints={'type': 'eq',
                                    'fun': self.f_eqcon,
                                    'args': (-1.0, )},
                       method='SLSQP', options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [1, 1])

    def test_minimize_equality_given(self):
        # Minimize with method='SLSQP': equality constraint, given jacobian.
        res = minimize(self.fun, [-1.0, 1.0], jac=self.jac,
                       method='SLSQP', args=(-1.0,),
                       constraints={'type': 'eq', 'fun':self.f_eqcon,
                                    'args': (-1.0, )},
                       options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [1, 1])

    def test_minimize_equality_given2(self):
        # Minimize with method='SLSQP': equality constraint, given jacobian
        # for fun and const.
        res = minimize(self.fun, [-1.0, 1.0], method='SLSQP',
                       jac=self.jac, args=(-1.0,),
                       constraints={'type': 'eq',
                                    'fun': self.f_eqcon,
                                    'args': (-1.0, ),
                                    'jac': self.fprime_eqcon},
                       options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [1, 1])

    def test_minimize_equality_given_cons_scalar(self):
        # Minimize with method='SLSQP': scalar equality constraint, given
        # jacobian for fun and const.
        res = minimize(self.fun, [-1.0, 1.0], method='SLSQP',
                       jac=self.jac, args=(-1.0,),
                       constraints={'type': 'eq',
                                    'fun': self.f_eqcon_scalar,
                                    'args': (-1.0, ),
                                    'jac': self.fprime_eqcon_scalar},
                       options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [1, 1])

    def test_minimize_inequality_given(self):
        # Minimize with method='SLSQP': inequality constraint, given jacobian.
        res = minimize(self.fun, [-1.0, 1.0], method='SLSQP',
                       jac=self.jac, args=(-1.0, ),
                       constraints={'type': 'ineq',
                                    'fun': self.f_ieqcon,
                                    'args': (-1.0, )},
                       options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [2, 1], atol=1e-3)

    def test_minimize_inequality_given_vector_constraints(self):
        # Minimize with method='SLSQP': vector inequality constraint, given
        # jacobian.
        res = minimize(self.fun, [-1.0, 1.0], jac=self.jac,
                       method='SLSQP', args=(-1.0,),
                       constraints={'type': 'ineq',
                                    'fun': self.f_ieqcon2,
                                    'jac': self.fprime_ieqcon2},
                       options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [2, 1])

    def test_minimize_bound_equality_given2(self):
        # Minimize with method='SLSQP': bounds, eq. const., given jac. for
        # fun. and const.
        res = minimize(self.fun, [-1.0, 1.0], method='SLSQP',
                       jac=self.jac, args=(-1.0, ),
                       bounds=[(-0.8, 1.), (-1, 0.8)],
                       constraints={'type': 'eq',
                                    'fun': self.f_eqcon,
                                    'args': (-1.0, ),
                                    'jac': self.fprime_eqcon},
                       options=self.opts)
        assert_(res['success'], res['message'])
        assert_allclose(res.x, [0.8, 0.8], atol=1e-3)
        assert_(-0.8 <= res.x[0] <= 1)
        assert_(-1 <= res.x[1] <= 0.8)

    # fmin_slsqp
    def test_unbounded_approximated(self):
        # SLSQP: unbounded, approximated jacobian.
        res = fmin_slsqp(self.fun, [-1.0, 1.0], args=(-1.0, ),
                         iprint = 0, full_output = 1)
        x, fx, its, imode, smode = res
        assert_(imode == 0, imode)
        assert_array_almost_equal(x, [2, 1])

    def test_unbounded_given(self):
        # SLSQP: unbounded, given jacobian.
        res = fmin_slsqp(self.fun, [-1.0, 1.0], args=(-1.0, ),
                         fprime = self.jac, iprint = 0,
                         full_output = 1)
        x, fx, its, imode, smode = res
        assert_(imode == 0, imode)
        assert_array_almost_equal(x, [2, 1])

    def test_equality_approximated(self):
        # SLSQP: equality constraint, approximated jacobian.
        res = fmin_slsqp(self.fun,[-1.0,1.0], args=(-1.0,),
                         eqcons = [self.f_eqcon],
                         iprint = 0, full_output = 1)
        x, fx, its, imode, smode = res
        assert_(imode == 0, imode)
        assert_array_almost_equal(x, [1, 1])

    def test_equality_given(self):
        # SLSQP: equality constraint, given jacobian.
        res = fmin_slsqp(self.fun, [-1.0, 1.0],
                         fprime=self.jac, args=(-1.0,),
                         eqcons = [self.f_eqcon], iprint = 0,
                         full_output = 1)
        x, fx, its, imode, smode = res
        assert_(imode == 0, imode)
        assert_array_almost_equal(x, [1, 1])

    def test_equality_given2(self):
        # SLSQP: equality constraint, given jacobian for fun and const.
        res = fmin_slsqp(self.fun, [-1.0, 1.0],
                         fprime=self.jac, args=(-1.0,),
                         f_eqcons = self.f_eqcon,
                         fprime_eqcons = self.fprime_eqcon,
                         iprint = 0,
                         full_output = 1)
        x, fx, its, imode, smode = res
        assert_(imode == 0, imode)
        assert_array_almost_equal(x, [1, 1])

    def test_inequality_given(self):
        # SLSQP: inequality constraint, given jacobian.
        res = fmin_slsqp(self.fun, [-1.0, 1.0],
                         fprime=self.jac, args=(-1.0, ),
                         ieqcons = [self.f_ieqcon],
                         iprint = 0, full_output = 1)
        x, fx, its, imode, smode = res
        assert_(imode == 0, imode)
        assert_array_almost_equal(x, [2, 1], decimal=3)

    def test_bound_equality_given2(self):
        # SLSQP: bounds, eq. const., given jac. for fun. and const.
        res = fmin_slsqp(self.fun, [-1.0, 1.0],
                         fprime=self.jac, args=(-1.0, ),
                         bounds = [(-0.8, 1.), (-1, 0.8)],
                         f_eqcons = self.f_eqcon,
                         fprime_eqcons = self.fprime_eqcon,
                         iprint = 0, full_output = 1)
        x, fx, its, imode, smode = res
        assert_(imode == 0, imode)
        assert_array_almost_equal(x, [0.8, 0.8], decimal=3)
        assert_(-0.8 <= x[0] <= 1)
        assert_(-1 <= x[1] <= 0.8)

    def test_scalar_constraints(self):
        # Regression test for gh-2182
        x = fmin_slsqp(lambda z: z**2, [3.],
                       ieqcons=[lambda z: z[0] - 1],
                       iprint=0)
        assert_array_almost_equal(x, [1.])

        x = fmin_slsqp(lambda z: z**2, [3.],
                       f_ieqcons=lambda z: [z[0] - 1],
                       iprint=0)
        assert_array_almost_equal(x, [1.])

    def test_integer_bounds(self):
        # This should not raise an exception
        fmin_slsqp(lambda z: z**2 - 1, [0], bounds=[[0, 1]], iprint=0)

    def test_callback(self):
        # Minimize, method='SLSQP': unbounded, approximated jacobian. Check for callback
        callback = MyCallBack()
        res = minimize(self.fun, [-1.0, 1.0], args=(-1.0, ),
                       method='SLSQP', callback=callback, options=self.opts)
        assert_(res['success'], res['message'])
        assert_(callback.been_called)
        assert_equal(callback.ncalls, res['nit'])


if __name__ == "__main__":
    run_module_suite()
