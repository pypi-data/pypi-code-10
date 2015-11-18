# coding: utf-8
"""Hybrid RBF-polynomial interpolation and approximation.
"""

# This code is a derived work from the file of the same name in
# the SciPy library, based closely on Matlab code by Alex Chirokov
# and
#
#   Copyright (c) 2006-2007, Robert Hetland <hetland@tamu.edu>
#   Copyright (c) 2007, John Travers <jtravs@gmail.com>
#
# with some additional alterations by Travis Oliphant.
#
# The modifications from the SciPy file are
#
#   Copyright (c) 2015, J.J. Green <j.j.green@gmx.co.uk>
#
# This code retains the licence as the original: the SciPy (BSD
# style) license: http://www.scipy.org/scipylib/license.html

import numpy as np
import scipy.spatial
import scipy.linalg
import warnings
from mvpoly.cube import MVPolyCube
from mvpoly.dict import MVPolyDict


class RBFBase(object):
    r"""Base class for radial basis functions

    A class for radial basis function approximation/interpolation of
    `n`-dimensional scattered data.

    Parameters
    ----------
    *args : arrays
        `x`, `y`, `z`, ..., `f`, where `x`, `y`, `z`, ... are the vectors
        of the coordinates of the nodes and `f` is the array of values at
        the nodes
    smooth : float, optional
        Values greater than zero increase the smoothness of the
        approximation.  The default value of zero gives interpolation, i.e.,
        the function will always go through the nodal points.
    poly_order : non-negative integer or `None`, optional (default 1)
        The order of a (low-order) polynomial to be fitted and added to the
        input data; the default of 1 corresponds to a linear term, 0 to a
        constant, `None` for no polynomial part.
    poly_class : one of the :class:`MVPoly` polynomial classes, optional

    Notes
    -----
    The base class is not used directly, instead one uses a subclass for
    which a particular basis function is defined,

    Examples
    --------
    For a set of `n` points in 3-dimensional space with coordinates
    in the `n`-vectors `x`, `y` and `z`; and with `f` being a
    `n`-vector of the data from which to interpolate, the interpolant
    `rbf` is created with

    >>> from mvpoly.rbf import RBFGauss
    >>> x, y, z, f = np.random.rand(4, 50)
    >>> rbf = RBFGauss(x, y, z, f)
    >>> rbf.name
    Gaussian
    """

    def _norm(self, x1, x2):
        return scipy.spatial.distance.cdist(x1.T, x2.T)

    def _mean_nearest_neighbour(self):
        kdtree = scipy.spatial.KDTree(self.xi.T)
        ds, _ = kdtree.query(self.xi.T, k=2)
        return np.mean(ds[:, 1])

    def _set_epsilon_default(self):
        self.epsilon = self._mean_nearest_neighbour()

    def _set_radius_default(self):
        self.radius = 2 * self._mean_nearest_neighbour()

    def _rbf_matrix(self):
        A = self.radial(self._norm(self.xi, self.xi))
        if self.smooth != 0.0:
            eigidx = 0 if self.sign < 0 else self.N - 1
            eig = scipy.linalg.eigh(A, eigvals_only=True,
                                    eigvals=(eigidx, eigidx))[0]
            A += np.eye(self.N) * self.smooth * eig
        return A

    def _poly_matrix(self, xa):
        if self.poly_order is None:
            return None
        if not self.poly_basis:
            self.poly_basis = self.poly_class.monomials(self.dim,
                                                        self.poly_order,
                                                        dtype=np.float64)
        K = np.vstack(p(*xa) for p in self.poly_basis)
        return K

    def __init__(self, *args, **kwargs):
        # the data points and the value of the function to be interpolated;
        xa = [np.asarray(a, dtype=np.float64).flatten() for a in args[:-1]]
        self.xi = np.asarray(xa)
        self.fi = np.asarray(args[-1]).flatten()

        if not all([x.size == self.fi.size for x in self.xi]):
            raise ValueError('All arrays must be equal length')

        # the dimension of the interpolation space, and the number of
        # interpolation samples
        self.dim = self.xi.shape[0]
        self.N = self.xi.shape[-1]

        # the shape parameter for some RBFs
        if self.needs_epsilon:
            self.epsilon = kwargs.pop('epsilon', None)
            if self.epsilon is None:
                self._set_epsilon_default()

        # the scaling factor for compactly supported RBFs
        if self.needs_radius:
            self.radius = kwargs.pop('radius', None)
            if self.radius is None:
                self._set_radius_default()

        # the smoothing parameter, if zero then the RBF will interpolate,
        # if non-zero then it will approximate.
        self.smooth = kwargs.pop('smooth', 0.0)

        # order of polynomial term ('None' for no polynomial term)
        self.poly_order = kwargs.pop('poly_order', 1)

        # polynomial class
        self.poly_class = kwargs.pop('poly_class', MVPolyDict)

        # polynomial basis (could be user defined without much effort)
        self.poly_basis = None

        # the interpolation (without the polynomial term)
        A = self._rbf_matrix()
        K = self._poly_matrix(xa)

        if K is None:

            self.rbf_coefs = np.linalg.solve(A, self.fi)
            self.poly = None

        else:

            nk = K.shape[0]
            Z = np.zeros((nk, nk), dtype=np.float64)
            A = np.vstack((np.hstack((A, K.T)), np.hstack((K, Z))))
            f = np.hstack((self.fi, np.zeros((nk,), dtype=np.float64)))
            coefs = np.linalg.solve(A, f)

            # RBF coefficients
            self.rbf_coefs = coefs[:self.N]

            # the polynomial
            poly_coefs = coefs[self.N:]
            self.poly = sum(c * p for c, p in zip(poly_coefs, self.poly_basis))

    def rbf(self, *args, **kwargs):
        large = kwargs.pop('large', False)
        shp = args[0].shape
        if not all([arg.shape == shp for arg in args]):
            raise ValueError('Array lengths must be equal')
        x = np.asarray([a.flatten() for a in args], dtype=np.float64)
        if large:
            return np.asarray([np.dot(self.radial(self._norm(m[:, np.newaxis],
                                                             self.xi)),
                                      self.rbf_coefs)
                               for m in x.T]).reshape(shp)
        else:
            r = self._norm(x, self.xi)
            return np.dot(self.radial(r), self.rbf_coefs).reshape(shp)

    def __call__(self, *args, **kwargs):
        """Evaluate the interpolant instance

        Parameters
        ----------
        *args : numbers or arrays
            The vectors components `x`, `y`, `z`, ... at which to evaluate
            the interpolant.  All must be the same shape.
        large : Boolean, optional (default `False`)
            Interpolation is performed iteratively rather than in a vectorised
            manner; this saves memory but is slower, use if there are a large
            number of sites on which to interpolate.

        Returns
        -------
        array
            A NumPy array which is the same shape as (each of the) input
            arguments.

        Examples
        --------
        With the interpolant `rbf` as defined in the example above, one
        can evaluate the interpolant at arbitrary points `xi`, `yi`, `zi`
        (in this case on a uniform grid) with

        >>> L = np.linspace(0, 1, 20)
        >>> xi, yi, zi = np.meshgrid(L, L, L)
        >>> fi = rbf(xi, yi, zi, large=False)
        >>> fi.shape
        (20, 20, 20)
        """
        large = kwargs.pop('large', False)
        args = [np.asarray(x, dtype=np.float64) for x in args]
        if len(args) == 0:
            raise ValueError('Need at least one argument')
        if self.poly is None:
            return self.rbf(*args, large=large)
        else:
            return self.rbf(*args, large=large) + self.poly(*args)


class RBFGaussian(RBFBase):
    r"""An RBF subclass for the *Gaussian* function

    .. math::

        \phi(r) = \exp\left(-(r/\epsilon)^2\right)

    The parameters are as for the base class :class:`RBFBase`, and
    in addition

    Parameters
    ----------
    epsilon : float, optional
        Adjustable constant modifying the shape of the radial function,
        if not specified then a value will be calculated which is
        approximately the average distance between adjacent nodes.
    """
    @property
    def name(self):
        """
        The name of the function
        """
        return 'Gaussian'

    @property
    def sign(self):
        return 1

    @property
    def needs_epsilon(self):
        return True

    @property
    def needs_radius(self):
        return False

    def radial(self, r):
        """
        The radial function itself
        """
        return np.exp(-(r / self.epsilon)**2)


class RBFMultiQuadric(RBFBase):
    r"""An RBF subclass for the *multiquadric* function

    .. math::

        \phi(r) = \sqrt{(r/\epsilon)^2 + 1}.

    The parameters are as for the base class :class:`RBFBase`, and
    in addition

    Parameters
    ----------
    epsilon : float, optional
        Adjustable constant modifying the shape of the radial function,
        if not specified then a value will be calculated which is
        approximately the average distance between adjacent nodes.
    """

    @property
    def name(self):
        """
        The name of the function
        """
        return 'multiquadric'

    @property
    def sign(self):
        return -1

    @property
    def needs_epsilon(self):
        return True

    @property
    def needs_radius(self):
        return False

    def radial(self, r):
        """
        The radial function itself
        """
        return np.sqrt((r / self.epsilon)**2 + 1)


class RBFInverseMultiQuadric(RBFBase):
    r"""An RBF subclass for the *inverse multiquadric*

    .. math::

        \phi(r) = \frac{1}{\sqrt{(r/\epsilon)^2 + 1}}.

    The parameters are as for the base class :class:`RBFBase`, and
    in addition

    Parameters
    ----------
    epsilon : float, optional
        Adjustable constant modifying the shape of the radial function,
        if not specified then a value will be calculated which is
        approximately the average distance between adjacent nodes.
    """
    @property
    def name(self):
        """
        The name of the function
        """
        return 'inverse multiquadric'

    @property
    def sign(self):
        return 1

    @property
    def needs_epsilon(self):
        return True

    @property
    def needs_radius(self):
        return False

    def radial(self, r):
        """
        The radial function itself
        """
        return 1.0 / np.sqrt((r / self.epsilon)**2 + 1)


class RBFThinPlateSpline(RBFBase):
    r"""An RBF subclass for the *thin-plate spline*

    .. math::

        \phi(r) = r^2 \log(r).

    The parameters are as for the base class :class:`RBFBase`.
    """
    @property
    def name(self):
        """
        The name of the function
        """
        return 'thin-plate spline'

    @property
    def sign(self):
        return 1

    @property
    def needs_epsilon(self):
        return False

    @property
    def needs_radius(self):
        return False

    def radial(self, r):
        """
        The radial function itself
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = r**2 * np.log(r)
        result[r == 0] = 0
        return result


class RBFWendland(RBFBase):
    r"""An RBF subclass for the *Wendland* function, a compactly
    supported basis funtion whose radial function is parametersed
    by the optional non-negative integer keyword argument *n*.
    The form of the polynomial depends on *n* and the dimension
    of the RBF; the larger the value of *n*, the smoother the
    interpolant. As an example, the radial function for *n=2* and
    RBF dimension one is

    .. math::

        \phi_{1, 2}(r) \propto (8r^2 + 5r + 1)(1 - r)^5
        \qquad
        (0 \leq r \leq 1)

    The parameters are as for the base class :class:`RBFBase`, and in
    addition

    Parameters
    ----------

    n : integer, optional
        A parameter controlling the order of the radial function,
        and the smoothness of the resulting interpolant (to be
        precise, the latter will be *2n*-times continuously
        differentiable.  If not specified a default value of 2
        will be used.

    radius : float, optional
        A scaling factor for the basis function, the radius of the
        support of the function. If not specified then a value will
        be calculated which is a small factor times an approximation
        of the average distance between adjacent nodes.

    Notes
    -----

    See also :func:`mvpoly.cube.MVPolyCube.wendland`.
    """

    def __init__(self, *args, **kwargs):
        self.n = kwargs.pop('n', 2)
        super(self.__class__, self).__init__(*args, **kwargs)

    @property
    def name(self):
        """
        The name of the function
        """
        return 'Wendland'

    @property
    def sign(self):
        return 1

    @property
    def needs_epsilon(self):
        return False

    @property
    def needs_radius(self):
        return True

    def radial(self, r):
        """
        The radial function itself
        """
        if not hasattr(self, 'wendland'):
            self.wendland = MVPolyCube.wendland(self.dim, self.n)

        # We perform the truncation of the radii (to the radius of
        # the support of the Wendland function) here, so that the
        # result is correct; but it is madness to use this facility,
        # the caller (i.e., __init__) should sparsify these values
        # away, since they know they will be zero.  This is planned.

        r0 = np.where(r < self.radius, r, self.radius)
        return self.wendland(r0 / self.radius)
