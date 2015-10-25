# Author:  Travis Oliphant, 2002
#
# Further updates and enhancements by many SciPy developers.
#
from __future__ import division, print_function, absolute_import

import math
import warnings
from collections import namedtuple

import numpy as np
from numpy import (isscalar, r_, log, sum, around, unique, asarray,
                   zeros, arange, sort, amin, amax, any, atleast_1d,
                   sqrt, ceil, floor, array, poly1d, compress,
                   pi, exp, ravel, angle, count_nonzero)
from numpy.testing.decorators import setastest

from scipy._lib.six import string_types
from scipy import optimize
from scipy import special
from . import statlib
from . import stats
from .stats import find_repeats
from .contingency import chi2_contingency
from . import distributions
from ._distn_infrastructure import rv_generic


__all__ = ['mvsdist',
           'bayes_mvs', 'kstat', 'kstatvar', 'probplot', 'ppcc_max', 'ppcc_plot',
           'boxcox_llf', 'boxcox', 'boxcox_normmax', 'boxcox_normplot',
           'shapiro', 'anderson', 'ansari', 'bartlett', 'levene', 'binom_test',
           'fligner', 'mood', 'wilcoxon', 'median_test',
           'pdf_fromgamma', 'circmean', 'circvar', 'circstd', 'anderson_ksamp'
           ]


Mean = namedtuple('Mean', ('statistic', 'minmax'))
Variance = namedtuple('Variance', ('statistic', 'minmax'))
Std_dev = namedtuple('Std_dev', ('statistic', 'minmax'))


def bayes_mvs(data, alpha=0.90):
    """
    Bayesian confidence intervals for the mean, var, and std.

    Parameters
    ----------
    data : array_like
        Input data, if multi-dimensional it is flattened to 1-D by `bayes_mvs`.
        Requires 2 or more data points.
    alpha : float, optional
        Probability that the returned confidence interval contains
        the true parameter.

    Returns
    -------
    mean_cntr, var_cntr, std_cntr : tuple
        The three results are for the mean, variance and standard deviation,
        respectively.  Each result is a tuple of the form::

            (center, (lower, upper))

        with `center` the mean of the conditional pdf of the value given the
        data, and `(lower, upper)` a confidence interval, centered on the
        median, containing the estimate to a probability ``alpha``.

    Notes
    -----
    Each tuple of mean, variance, and standard deviation estimates represent
    the (center, (lower, upper)) with center the mean of the conditional pdf
    of the value given the data and (lower, upper) is a confidence interval
    centered on the median, containing the estimate to a probability
    ``alpha``.

    Converts data to 1-D and assumes all data has the same mean and variance.
    Uses Jeffrey's prior for variance and std.

    Equivalent to ``tuple((x.mean(), x.interval(alpha)) for x in mvsdist(dat))``

    References
    ----------
    T.E. Oliphant, "A Bayesian perspective on estimating mean, variance, and
    standard-deviation from data", http://hdl.handle.net/1877/438, 2006.

    """
    m, v, s = mvsdist(data)
    if alpha >= 1 or alpha <= 0:
        raise ValueError("0 < alpha < 1 is required, but alpha=%s was given."
                         % alpha)

    m_res = Mean(m.mean(), m.interval(alpha))
    v_res = Variance(v.mean(), v.interval(alpha))
    s_res = Std_dev(s.mean(), s.interval(alpha))

    return m_res, v_res, s_res


def mvsdist(data):
    """
    'Frozen' distributions for mean, variance, and standard deviation of data.

    Parameters
    ----------
    data : array_like
        Input array. Converted to 1-D using ravel.
        Requires 2 or more data-points.

    Returns
    -------
    mdist : "frozen" distribution object
        Distribution object representing the mean of the data
    vdist : "frozen" distribution object
        Distribution object representing the variance of the data
    sdist : "frozen" distribution object
        Distribution object representing the standard deviation of the data

    Notes
    -----
    The return values from bayes_mvs(data) is equivalent to
    ``tuple((x.mean(), x.interval(0.90)) for x in mvsdist(data))``.

    In other words, calling ``<dist>.mean()`` and ``<dist>.interval(0.90)``
    on the three distribution objects returned from this function will give
    the same results that are returned from `bayes_mvs`.

    Examples
    --------
    >>> from scipy import stats
    >>> data = [6, 9, 12, 7, 8, 8, 13]
    >>> mean, var, std = stats.mvsdist(data)

    We now have frozen distribution objects "mean", "var" and "std" that we can
    examine:

    >>> mean.mean()
    9.0
    >>> mean.interval(0.95)
    (6.6120585482655692, 11.387941451734431)
    >>> mean.std()
    1.1952286093343936

    """
    x = ravel(data)
    n = len(x)
    if n < 2:
        raise ValueError("Need at least 2 data-points.")
    xbar = x.mean()
    C = x.var()
    if n > 1000:  # gaussian approximations for large n
        mdist = distributions.norm(loc=xbar, scale=math.sqrt(C / n))
        sdist = distributions.norm(loc=math.sqrt(C), scale=math.sqrt(C / (2. * n)))
        vdist = distributions.norm(loc=C, scale=math.sqrt(2.0 / n) * C)
    else:
        nm1 = n - 1
        fac = n * C / 2.
        val = nm1 / 2.
        mdist = distributions.t(nm1, loc=xbar, scale=math.sqrt(C / nm1))
        sdist = distributions.gengamma(val, -2, scale=math.sqrt(fac))
        vdist = distributions.invgamma(val, scale=fac)
    return mdist, vdist, sdist


def kstat(data, n=2):
    """
    Return the nth k-statistic (1<=n<=4 so far).

    The nth k-statistic is the unique symmetric unbiased estimator of the nth
    cumulant kappa_n.

    Parameters
    ----------
    data : array_like
        Input array.
    n : int, {1, 2, 3, 4}, optional
        Default is equal to 2.

    Returns
    -------
    kstat : float
        The nth k-statistic.

    See Also
    --------
    kstatvar: Returns an unbiased estimator of the variance of the k-statistic.

    Notes
    -----
    The cumulants are related to central moments but are specifically defined
    using a power series expansion of the logarithm of the characteristic
    function (which is the Fourier transform of the PDF).
    In particular let phi(t) be the characteristic function, then::

        ln phi(t) = > kappa_n (it)^n / n!    (sum from n=0 to inf)

    The first few cumulants (kappa_n)  in terms of central moments (mu_n) are::

        kappa_1 = mu_1
        kappa_2 = mu_2
        kappa_3 = mu_3
        kappa_4 = mu_4 - 3*mu_2**2
        kappa_5 = mu_5 - 10*mu_2 * mu_3

    References
    ----------
    http://mathworld.wolfram.com/k-Statistic.html

    http://mathworld.wolfram.com/Cumulant.html

    """
    if n > 4 or n < 1:
        raise ValueError("k-statistics only supported for 1<=n<=4")
    n = int(n)
    S = zeros(n + 1, 'd')
    data = ravel(data)
    N = len(data)
    for k in range(1, n + 1):
        S[k] = sum(data**k, axis=0)
    if n == 1:
        return S[1] * 1.0/N
    elif n == 2:
        return (N*S[2] - S[1]**2.0) / (N*(N - 1.0))
    elif n == 3:
        return (2*S[1]**3 - 3*N*S[1]*S[2] + N*N*S[3]) / (N*(N - 1.0)*(N - 2.0))
    elif n == 4:
        return ((-6*S[1]**4 + 12*N*S[1]**2 * S[2] - 3*N*(N-1.0)*S[2]**2 -
                 4*N*(N+1)*S[1]*S[3] + N*N*(N+1)*S[4]) /
                 (N*(N-1.0)*(N-2.0)*(N-3.0)))
    else:
        raise ValueError("Should not be here.")


def kstatvar(data, n=2):
    """
    Returns an unbiased estimator of the variance of the k-statistic.

    See `kstat` for more details of the k-statistic.

    Parameters
    ----------
    data : array_like
        Input array.
    n : int, {1, 2}, optional
        Default is equal to 2.

    Returns
    -------
    kstatvar : float
        The nth k-statistic variance.

    See Also
    --------
    kstat

    """
    data = ravel(data)
    N = len(data)
    if n == 1:
        return kstat(data, n=2) * 1.0/N
    elif n == 2:
        k2 = kstat(data, n=2)
        k4 = kstat(data, n=4)
        return (2*N*k2**2 + (N-1)*k4) / (N*(N+1))
    else:
        raise ValueError("Only n=1 or n=2 supported.")


def _calc_uniform_order_statistic_medians(x):
    """See Notes section of `probplot` for details."""
    N = len(x)
    osm_uniform = np.zeros(N, dtype=np.float64)
    osm_uniform[-1] = 0.5**(1.0 / N)
    osm_uniform[0] = 1 - osm_uniform[-1]
    i = np.arange(2, N)
    osm_uniform[1:-1] = (i - 0.3175) / (N + 0.365)
    return osm_uniform


def _parse_dist_kw(dist, enforce_subclass=True):
    """Parse `dist` keyword.

    Parameters
    ----------
    dist : str or stats.distributions instance.
        Several functions take `dist` as a keyword, hence this utility
        function.
    enforce_subclass : bool, optional
        If True (default), `dist` needs to be a
        `_distn_infrastructure.rv_generic` instance.
        It can sometimes be useful to set this keyword to False, if a function
        wants to accept objects that just look somewhat like such an instance
        (for example, they have a ``ppf`` method).

    """
    if isinstance(dist, rv_generic):
        pass
    elif isinstance(dist, string_types):
        try:
            dist = getattr(distributions, dist)
        except AttributeError:
            raise ValueError("%s is not a valid distribution name" % dist)
    elif enforce_subclass:
        msg = ("`dist` should be a stats.distributions instance or a string "
               "with the name of such a distribution.")
        raise ValueError(msg)

    return dist


def _add_axis_labels_title(plot, xlabel, ylabel, title):
    """Helper function to add axes labels and a title to stats plots"""
    try:
        if hasattr(plot, 'set_title'):
            # Matplotlib Axes instance or something that looks like it
            plot.set_title(title)
            plot.set_xlabel(xlabel)
            plot.set_ylabel(ylabel)
        else:
            # matplotlib.pyplot module
            plot.title(title)
            plot.xlabel(xlabel)
            plot.ylabel(ylabel)
    except:
        # Not an MPL object or something that looks (enough) like it.
        # Don't crash on adding labels or title
        pass


def probplot(x, sparams=(), dist='norm', fit=True, plot=None):
    """
    Calculate quantiles for a probability plot, and optionally show the plot.

    Generates a probability plot of sample data against the quantiles of a
    specified theoretical distribution (the normal distribution by default).
    `probplot` optionally calculates a best-fit line for the data and plots the
    results using Matplotlib or a given plot function.

    Parameters
    ----------
    x : array_like
        Sample/response data from which `probplot` creates the plot.
    sparams : tuple, optional
        Distribution-specific shape parameters (shape parameters plus location
        and scale).
    dist : str or stats.distributions instance, optional
        Distribution or distribution function name. The default is 'norm' for a
        normal probability plot.  Objects that look enough like a
        stats.distributions instance (i.e. they have a ``ppf`` method) are also
        accepted.
    fit : bool, optional
        Fit a least-squares regression (best-fit) line to the sample data if
        True (default).
    plot : object, optional
        If given, plots the quantiles and least squares fit.
        `plot` is an object that has to have methods "plot" and "text".
        The `matplotlib.pyplot` module or a Matplotlib Axes object can be used,
        or a custom object with the same methods.
        Default is None, which means that no plot is created.

    Returns
    -------
    (osm, osr) : tuple of ndarrays
        Tuple of theoretical quantiles (osm, or order statistic medians) and
        ordered responses (osr).  `osr` is simply sorted input `x`.
        For details on how `osm` is calculated see the Notes section.
    (slope, intercept, r) : tuple of floats, optional
        Tuple  containing the result of the least-squares fit, if that is
        performed by `probplot`. `r` is the square root of the coefficient of
        determination.  If ``fit=False`` and ``plot=None``, this tuple is not
        returned.

    Notes
    -----
    Even if `plot` is given, the figure is not shown or saved by `probplot`;
    ``plt.show()`` or ``plt.savefig('figname.png')`` should be used after
    calling `probplot`.

    `probplot` generates a probability plot, which should not be confused with
    a Q-Q or a P-P plot.  Statsmodels has more extensive functionality of this
    type, see ``statsmodels.api.ProbPlot``.

    The formula used for the theoretical quantiles (horizontal axis of the
    probability plot) is Filliben's estimate::

        quantiles = dist.ppf(val), for

                0.5**(1/n),                  for i = n
          val = (i - 0.3175) / (n + 0.365),  for i = 2, ..., n-1
                1 - 0.5**(1/n),              for i = 1

    where ``i`` indicates the i-th ordered value and ``n`` is the total number
    of values.

    Examples
    --------
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt
    >>> nsample = 100
    >>> np.random.seed(7654321)

    A t distribution with small degrees of freedom:

    >>> ax1 = plt.subplot(221)
    >>> x = stats.t.rvs(3, size=nsample)
    >>> res = stats.probplot(x, plot=plt)

    A t distribution with larger degrees of freedom:

    >>> ax2 = plt.subplot(222)
    >>> x = stats.t.rvs(25, size=nsample)
    >>> res = stats.probplot(x, plot=plt)

    A mixture of two normal distributions with broadcasting:

    >>> ax3 = plt.subplot(223)
    >>> x = stats.norm.rvs(loc=[0,5], scale=[1,1.5],
    ...                    size=(nsample/2.,2)).ravel()
    >>> res = stats.probplot(x, plot=plt)

    A standard normal distribution:

    >>> ax4 = plt.subplot(224)
    >>> x = stats.norm.rvs(loc=0, scale=1, size=nsample)
    >>> res = stats.probplot(x, plot=plt)

    Produce a new figure with a loggamma distribution, using the ``dist`` and
    ``sparams`` keywords:

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> x = stats.loggamma.rvs(c=2.5, size=500)
    >>> stats.probplot(x, dist=stats.loggamma, sparams=(2.5,), plot=ax)
    >>> ax.set_title("Probplot for loggamma dist with shape parameter 2.5")

    Show the results with Matplotlib:

    >>> plt.show()

    """
    x = np.asarray(x)
    _perform_fit = fit or (plot is not None)
    if x.size == 0:
        if _perform_fit:
            return (x, x), (np.nan, np.nan, 0.0)
        else:
            return x, x

    osm_uniform = _calc_uniform_order_statistic_medians(x)
    dist = _parse_dist_kw(dist, enforce_subclass=False)
    if sparams is None:
        sparams = ()
    if isscalar(sparams):
        sparams = (sparams,)
    if not isinstance(sparams, tuple):
        sparams = tuple(sparams)

    osm = dist.ppf(osm_uniform, *sparams)
    osr = sort(x)
    if _perform_fit:
        # perform a linear least squares fit.
        slope, intercept, r, prob, sterrest = stats.linregress(osm, osr)

    if plot is not None:
        plot.plot(osm, osr, 'bo', osm, slope*osm + intercept, 'r-')
        _add_axis_labels_title(plot, xlabel='Quantiles',
                               ylabel='Ordered Values',
                               title='Probability Plot')

        # Add R^2 value to the plot as text
        xmin = amin(osm)
        xmax = amax(osm)
        ymin = amin(x)
        ymax = amax(x)
        posx = xmin + 0.70 * (xmax - xmin)
        posy = ymin + 0.01 * (ymax - ymin)
        plot.text(posx, posy, "$R^2=%1.4f$" % r**2)

    if fit:
        return (osm, osr), (slope, intercept, r)
    else:
        return osm, osr


def ppcc_max(x, brack=(0.0, 1.0), dist='tukeylambda'):
    """Returns the shape parameter that maximizes the probability plot
    correlation coefficient for the given data to a one-parameter
    family of distributions.

    See also ppcc_plot
    """
    dist = _parse_dist_kw(dist)
    osm_uniform = _calc_uniform_order_statistic_medians(x)
    osr = sort(x)

    # this function computes the x-axis values of the probability plot
    #  and computes a linear regression (including the correlation)
    #  and returns 1-r so that a minimization function maximizes the
    #  correlation
    def tempfunc(shape, mi, yvals, func):
        xvals = func(mi, shape)
        r, prob = stats.pearsonr(xvals, yvals)
        return 1 - r

    return optimize.brent(tempfunc, brack=brack, args=(osm_uniform, osr, dist.ppf))


def ppcc_plot(x, a, b, dist='tukeylambda', plot=None, N=80):
    """
    Calculate and optionally plot probability plot correlation coefficient.

    The probability plot correlation coefficient (PPCC) plot can be used to
    determine the optimal shape parameter for a one-parameter family of
    distributions.  It cannot be used for distributions without shape parameters
    (like the normal distribution) or with multiple shape parameters.

    By default a Tukey-Lambda distribution (`stats.tukeylambda`) is used. A
    Tukey-Lambda PPCC plot interpolates from long-tailed to short-tailed
    distributions via an approximately normal one, and is therefore particularly
    useful in practice.

    Parameters
    ----------
    x : array_like
        Input array.
    a, b: scalar
        Lower and upper bounds of the shape parameter to use.
    dist : str or stats.distributions instance, optional
        Distribution or distribution function name.  Objects that look enough
        like a stats.distributions instance (i.e. they have a ``ppf`` method)
        are also accepted.  The default is ``'tukeylambda'``.
    plot : object, optional
        If given, plots PPCC against the shape parameter.
        `plot` is an object that has to have methods "plot" and "text".
        The `matplotlib.pyplot` module or a Matplotlib Axes object can be used,
        or a custom object with the same methods.
        Default is None, which means that no plot is created.
    N : int, optional
        Number of points on the horizontal axis (equally distributed from
        `a` to `b`).

    Returns
    -------
    svals : ndarray
        The shape values for which `ppcc` was calculated.
    ppcc : ndarray
        The calculated probability plot correlation coefficient values.

    See also
    --------
    ppcc_max, probplot, boxcox_normplot, tukeylambda

    References
    ----------
    J.J. Filliben, "The Probability Plot Correlation Coefficient Test for
    Normality", Technometrics, Vol. 17, pp. 111-117, 1975.

    Examples
    --------
    First we generate some random data from a Tukey-Lambda distribution,
    with shape parameter -0.7:

    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt
    >>> np.random.seed(1234567)
    >>> x = stats.tukeylambda.rvs(-0.7, loc=2, scale=0.5, size=10000) + 1e4

    Now we explore this data with a PPCC plot as well as the related
    probability plot and Box-Cox normplot.  A red line is drawn where we
    expect the PPCC value to be maximal (at the shape parameter -0.7 used
    above):

    >>> fig = plt.figure(figsize=(12, 4))
    >>> ax1 = fig.add_subplot(131)
    >>> ax2 = fig.add_subplot(132)
    >>> ax3 = fig.add_subplot(133)
    >>> stats.probplot(x, plot=ax1)
    >>> stats.boxcox_normplot(x, -5, 5, plot=ax2)
    >>> stats.ppcc_plot(x, -5, 5, plot=ax3)
    >>> ax3.vlines(-0.7, 0, 1, colors='r', label='Expected shape value')
    >>> plt.show()

    """
    if b <= a:
        raise ValueError("`b` has to be larger than `a`.")

    svals = np.linspace(a, b, num=N)
    ppcc = np.empty_like(svals)
    for k, sval in enumerate(svals):
        _, r2 = probplot(x, sval, dist=dist, fit=True)
        ppcc[k] = r2[-1]

    if plot is not None:
        plot.plot(svals, ppcc, 'x')
        _add_axis_labels_title(plot, xlabel='Shape Values',
                               ylabel='Prob Plot Corr. Coef.',
                               title='(%s) PPCC Plot' % dist)

    return svals, ppcc


def boxcox_llf(lmb, data):
    r"""The boxcox log-likelihood function.

    Parameters
    ----------
    lmb : scalar
        Parameter for Box-Cox transformation.  See `boxcox` for details.
    data : array_like
        Data to calculate Box-Cox log-likelihood for.  If `data` is
        multi-dimensional, the log-likelihood is calculated along the first
        axis.

    Returns
    -------
    llf : float or ndarray
        Box-Cox log-likelihood of `data` given `lmb`.  A float for 1-D `data`,
        an array otherwise.

    See Also
    --------
    boxcox, probplot, boxcox_normplot, boxcox_normmax

    Notes
    -----
    The Box-Cox log-likelihood function is defined here as

    .. math::

        llf = (\lambda - 1) \sum_i(\log(x_i)) -
              N/2 \log(\sum_i (y_i - \bar{y})^2 / N),

    where ``y`` is the Box-Cox transformed input data ``x``.

    Examples
    --------
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt
    >>> from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    >>> np.random.seed(1245)

    Generate some random variates and calculate Box-Cox log-likelihood values
    for them for a range of ``lmbda`` values:

    >>> x = stats.loggamma.rvs(5, loc=10, size=1000)
    >>> lmbdas = np.linspace(-2, 10)
    >>> llf = np.zeros(lmbdas.shape, dtype=np.float)
    >>> for ii, lmbda in enumerate(lmbdas):
    ...     llf[ii] = stats.boxcox_llf(lmbda, x)

    Also find the optimal lmbda value with `boxcox`:

    >>> x_most_normal, lmbda_optimal = stats.boxcox(x)

    Plot the log-likelihood as function of lmbda.  Add the optimal lmbda as a
    horizontal line to check that that's really the optimum:

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> ax.plot(lmbdas, llf, 'b.-')
    >>> ax.axhline(stats.boxcox_llf(lmbda_optimal, x), color='r')
    >>> ax.set_xlabel('lmbda parameter')
    >>> ax.set_ylabel('Box-Cox log-likelihood')

    Now add some probability plots to show that where the log-likelihood is
    maximized the data transformed with `boxcox` looks closest to normal:

    >>> locs = [3, 10, 4]  # 'lower left', 'center', 'lower right'
    >>> for lmbda, loc in zip([-1, lmbda_optimal, 9], locs):
    ...     xt = stats.boxcox(x, lmbda=lmbda)
    ...     (osm, osr), (slope, intercept, r_sq) = stats.probplot(xt)
    ...     ax_inset = inset_axes(ax, width="20%", height="20%", loc=loc)
    ...     ax_inset.plot(osm, osr, 'c.', osm, slope*osm + intercept, 'k-')
    ...     ax_inset.set_xticklabels([])
    ...     ax_inset.set_yticklabels([])
    ...     ax_inset.set_title('$\lambda=%1.2f$' % lmbda)

    >>> plt.show()

    """
    data = np.asarray(data)
    N = data.shape[0]
    if N == 0:
        return np.nan

    y = boxcox(data, lmb)
    y_mean = np.mean(y, axis=0)
    llf = (lmb - 1) * np.sum(np.log(data), axis=0)
    llf -= N / 2.0 * np.log(np.sum((y - y_mean)**2. / N, axis=0))
    return llf


def _boxcox_conf_interval(x, lmax, alpha):
    # Need to find the lambda for which
    #  f(x,lmbda) >= f(x,lmax) - 0.5*chi^2_alpha;1
    fac = 0.5 * distributions.chi2.ppf(1 - alpha, 1)
    target = boxcox_llf(lmax, x) - fac

    def rootfunc(lmbda, data, target):
        return boxcox_llf(lmbda, data) - target

    # Find positive endpoint of interval in which answer is to be found
    newlm = lmax + 0.5
    N = 0
    while (rootfunc(newlm, x, target) > 0.0) and (N < 500):
        newlm += 0.1
        N += 1

    if N == 500:
        raise RuntimeError("Could not find endpoint.")

    lmplus = optimize.brentq(rootfunc, lmax, newlm, args=(x, target))

    # Now find negative interval in the same way
    newlm = lmax - 0.5
    N = 0
    while (rootfunc(newlm, x, target) > 0.0) and (N < 500):
        newlm -= 0.1
        N += 1

    if N == 500:
        raise RuntimeError("Could not find endpoint.")

    lmminus = optimize.brentq(rootfunc, newlm, lmax, args=(x, target))
    return lmminus, lmplus


def boxcox(x, lmbda=None, alpha=None):
    r"""
    Return a positive dataset transformed by a Box-Cox power transformation.

    Parameters
    ----------
    x : ndarray
        Input array.  Should be 1-dimensional.
    lmbda : {None, scalar}, optional
        If `lmbda` is not None, do the transformation for that value.

        If `lmbda` is None, find the lambda that maximizes the log-likelihood
        function and return it as the second output argument.
    alpha : {None, float}, optional
        If ``alpha`` is not None, return the ``100 * (1-alpha)%`` confidence
        interval for `lmbda` as the third output argument.
        Must be between 0.0 and 1.0.

    Returns
    -------
    boxcox : ndarray
        Box-Cox power transformed array.
    maxlog : float, optional
        If the `lmbda` parameter is None, the second returned argument is
        the lambda that maximizes the log-likelihood function.
    (min_ci, max_ci) : tuple of float, optional
        If `lmbda` parameter is None and ``alpha`` is not None, this returned
        tuple of floats represents the minimum and maximum confidence limits
        given ``alpha``.

    See Also
    --------
    probplot, boxcox_normplot, boxcox_normmax, boxcox_llf

    Notes
    -----
    The Box-Cox transform is given by::

        y = (x**lmbda - 1) / lmbda,  for lmbda > 0
            log(x),                  for lmbda = 0

    `boxcox` requires the input data to be positive.  Sometimes a Box-Cox
    transformation provides a shift parameter to achieve this; `boxcox` does
    not.  Such a shift parameter is equivalent to adding a positive constant to
    `x` before calling `boxcox`.

    The confidence limits returned when ``alpha`` is provided give the interval
    where:

    .. math::

        llf(\hat{\lambda}) - llf(\lambda) < \frac{1}{2}\chi^2(1 - \alpha, 1),

    with ``llf`` the log-likelihood function and :math:`\chi^2` the chi-squared
    function.

    References
    ----------
    G.E.P. Box and D.R. Cox, "An Analysis of Transformations", Journal of the
    Royal Statistical Society B, 26, 211-252 (1964).

    Examples
    --------
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt

    We generate some random variates from a non-normal distribution and make a
    probability plot for it, to show it is non-normal in the tails:

    >>> fig = plt.figure()
    >>> ax1 = fig.add_subplot(211)
    >>> x = stats.loggamma.rvs(5, size=500) + 5
    >>> stats.probplot(x, dist=stats.norm, plot=ax1)
    >>> ax1.set_xlabel('')
    >>> ax1.set_title('Probplot against normal distribution')

    We now use `boxcox` to transform the data so it's closest to normal:

    >>> ax2 = fig.add_subplot(212)
    >>> xt, _ = stats.boxcox(x)
    >>> stats.probplot(xt, dist=stats.norm, plot=ax2)
    >>> ax2.set_title('Probplot after Box-Cox transformation')

    >>> plt.show()

    """
    x = np.asarray(x)
    if x.size == 0:
        return x

    if any(x <= 0):
        raise ValueError("Data must be positive.")

    if lmbda is not None:  # single transformation
        return special.boxcox(x, lmbda)

    # If lmbda=None, find the lmbda that maximizes the log-likelihood function.
    lmax = boxcox_normmax(x, method='mle')
    y = boxcox(x, lmax)

    if alpha is None:
        return y, lmax
    else:
        # Find confidence interval
        interval = _boxcox_conf_interval(x, lmax, alpha)
        return y, lmax, interval


def boxcox_normmax(x, brack=(-2.0, 2.0), method='pearsonr'):
    """Compute optimal Box-Cox transform parameter for input data.

    Parameters
    ----------
    x : array_like
        Input array.
    brack : 2-tuple, optional
        The starting interval for a downhill bracket search with
        `optimize.brent`.  Note that this is in most cases not critical; the
        final result is allowed to be outside this bracket.
    method : str, optional
        The method to determine the optimal transform parameter (`boxcox`
        ``lmbda`` parameter). Options are:

        'pearsonr'  (default)
            Maximizes the Pearson correlation coefficient between
            ``y = boxcox(x)`` and the expected values for ``y`` if `x` would be
            normally-distributed.

        'mle'
            Minimizes the log-likelihood `boxcox_llf`.  This is the method used
            in `boxcox`.

        'all'
            Use all optimization methods available, and return all results.
            Useful to compare different methods.

    Returns
    -------
    maxlog : float or ndarray
        The optimal transform parameter found.  An array instead of a scalar
        for ``method='all'``.

    See Also
    --------
    boxcox, boxcox_llf, boxcox_normplot

    Examples
    --------
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt
    >>> np.random.seed(1234)  # make this example reproducible

    Generate some data and determine optimal ``lmbda`` in various ways:

    >>> x = stats.loggamma.rvs(5, size=30) + 5
    >>> y, lmax_mle = stats.boxcox(x)
    >>> lmax_pearsonr = stats.boxcox_normmax(x)

    >>> lmax_mle
    7.177...
    >>> lmax_pearsonr
    7.916...
    >>> stats.boxcox_normmax(x, method='all')
    array([ 7.91667384,  7.17718692])

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> stats.boxcox_normplot(x, -10, 10, plot=ax)
    >>> ax.axvline(lmax_mle, color='r')
    >>> ax.axvline(lmax_pearsonr, color='g', ls='--')

    >>> plt.show()

    """

    def _pearsonr(x, brack):
        osm_uniform = _calc_uniform_order_statistic_medians(x)
        xvals = distributions.norm.ppf(osm_uniform)

        def _eval_pearsonr(lmbda, xvals, samps):
            # This function computes the x-axis values of the probability plot
            # and computes a linear regression (including the correlation) and
            # returns ``1 - r`` so that a minimization function maximizes the
            # correlation.
            y = boxcox(samps, lmbda)
            yvals = np.sort(y)
            r, prob = stats.pearsonr(xvals, yvals)
            return 1 - r

        return optimize.brent(_eval_pearsonr, brack=brack, args=(xvals, x))

    def _mle(x, brack):
        def _eval_mle(lmb, data):
            # function to minimize
            return -boxcox_llf(lmb, data)

        return optimize.brent(_eval_mle, brack=brack, args=(x,))

    def _all(x, brack):
        maxlog = np.zeros(2, dtype=np.float)
        maxlog[0] = _pearsonr(x, brack)
        maxlog[1] = _mle(x, brack)
        return maxlog

    methods = {'pearsonr': _pearsonr,
               'mle': _mle,
               'all': _all}
    if method not in methods.keys():
        raise ValueError("Method %s not recognized." % method)

    optimfunc = methods[method]
    return optimfunc(x, brack)


def boxcox_normplot(x, la, lb, plot=None, N=80):
    """Compute parameters for a Box-Cox normality plot, optionally show it.

    A Box-Cox normality plot shows graphically what the best transformation
    parameter is to use in `boxcox` to obtain a distribution that is close
    to normal.

    Parameters
    ----------
    x : array_like
        Input array.
    la, lb : scalar
        The lower and upper bounds for the ``lmbda`` values to pass to `boxcox`
        for Box-Cox transformations.  These are also the limits of the
        horizontal axis of the plot if that is generated.
    plot : object, optional
        If given, plots the quantiles and least squares fit.
        `plot` is an object that has to have methods "plot" and "text".
        The `matplotlib.pyplot` module or a Matplotlib Axes object can be used,
        or a custom object with the same methods.
        Default is None, which means that no plot is created.
    N : int, optional
        Number of points on the horizontal axis (equally distributed from
        `la` to `lb`).

    Returns
    -------
    lmbdas : ndarray
        The ``lmbda`` values for which a Box-Cox transform was done.
    ppcc : ndarray
        Probability Plot Correlelation Coefficient, as obtained from `probplot`
        when fitting the Box-Cox transformed input `x` against a normal
        distribution.

    See Also
    --------
    probplot, boxcox, boxcox_normmax, boxcox_llf, ppcc_max

    Notes
    -----
    Even if `plot` is given, the figure is not shown or saved by
    `boxcox_normplot`; ``plt.show()`` or ``plt.savefig('figname.png')``
    should be used after calling `probplot`.

    Examples
    --------
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt

    Generate some non-normally distributed data, and create a Box-Cox plot:

    >>> x = stats.loggamma.rvs(5, size=500) + 5
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> stats.boxcox_normplot(x, -20, 20, plot=ax)

    Determine and plot the optimal ``lmbda`` to transform ``x`` and plot it in
    the same plot:

    >>> _, maxlog = stats.boxcox(x)
    >>> ax.axvline(maxlog, color='r')

    >>> plt.show()

    """
    x = np.asarray(x)
    if x.size == 0:
        return x

    if lb <= la:
        raise ValueError("`lb` has to be larger than `la`.")

    lmbdas = np.linspace(la, lb, num=N)
    ppcc = lmbdas * 0.0
    for i, val in enumerate(lmbdas):
        # Determine for each lmbda the correlation coefficient of transformed x
        z = boxcox(x, lmbda=val)
        _, r2 = probplot(z, dist='norm', fit=True)
        ppcc[i] = r2[-1]

    if plot is not None:
        plot.plot(lmbdas, ppcc, 'x')
        _add_axis_labels_title(plot, xlabel='$\lambda$',
                               ylabel='Prob Plot Corr. Coef.',
                               title='Box-Cox Normality Plot')

    return lmbdas, ppcc


def shapiro(x, a=None, reta=False):
    """
    Perform the Shapiro-Wilk test for normality.

    The Shapiro-Wilk test tests the null hypothesis that the
    data was drawn from a normal distribution.

    Parameters
    ----------
    x : array_like
        Array of sample data.
    a : array_like, optional
        Array of internal parameters used in the calculation.  If these
        are not given, they will be computed internally.  If x has length
        n, then a must have length n/2.
    reta : bool, optional
        Whether or not to return the internally computed a values.  The
        default is False.

    Returns
    -------
    W : float
        The test statistic.
    p-value : float
        The p-value for the hypothesis test.
    a : array_like, optional
        If `reta` is True, then these are the internally computed "a"
        values that may be passed into this function on future calls.

    See Also
    --------
    anderson : The Anderson-Darling test for normality

    References
    ----------
    .. [1] http://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm

    """
    N = len(x)
    if N < 3:
        raise ValueError("Data must be at least length 3.")
    if a is None:
        a = zeros(N, 'f')
        init = 0
    else:
        if len(a) != N // 2:
            raise ValueError("len(a) must equal len(x)/2")
        init = 1
    y = sort(x)
    a, w, pw, ifault = statlib.swilk(y, a[:N//2], init)
    if ifault not in [0, 2]:
        warnings.warn(str(ifault))
    if N > 5000:
        warnings.warn("p-value may not be accurate for N > 5000.")
    if reta:
        return w, pw, a
    else:
        return w, pw

# Values from Stephens, M A, "EDF Statistics for Goodness of Fit and
#             Some Comparisons", Journal of he American Statistical
#             Association, Vol. 69, Issue 347, Sept. 1974, pp 730-737
_Avals_norm = array([0.576, 0.656, 0.787, 0.918, 1.092])
_Avals_expon = array([0.922, 1.078, 1.341, 1.606, 1.957])
# From Stephens, M A, "Goodness of Fit for the Extreme Value Distribution",
#             Biometrika, Vol. 64, Issue 3, Dec. 1977, pp 583-588.
_Avals_gumbel = array([0.474, 0.637, 0.757, 0.877, 1.038])
# From Stephens, M A, "Tests of Fit for the Logistic Distribution Based
#             on the Empirical Distribution Function.", Biometrika,
#             Vol. 66, Issue 3, Dec. 1979, pp 591-595.
_Avals_logistic = array([0.426, 0.563, 0.660, 0.769, 0.906, 1.010])


AndersonResult = namedtuple('AndersonResult', ('statistic',
                                               'critical_values',
                                               'significance_level'))


def anderson(x, dist='norm'):
    """
    Anderson-Darling test for data coming from a particular distribution

    The Anderson-Darling test is a modification of the Kolmogorov-
    Smirnov test `kstest` for the null hypothesis that a sample is
    drawn from a population that follows a particular distribution.
    For the Anderson-Darling test, the critical values depend on
    which distribution is being tested against.  This function works
    for normal, exponential, logistic, or Gumbel (Extreme Value
    Type I) distributions.

    Parameters
    ----------
    x : array_like
        array of sample data
    dist : {'norm','expon','logistic','gumbel','extreme1'}, optional
        the type of distribution to test against.  The default is 'norm'
        and 'extreme1' is a synonym for 'gumbel'

    Returns
    -------
    statistic : float
        The Anderson-Darling test statistic
    critical_values : list
        The critical values for this distribution
    significance_level : list
        The significance levels for the corresponding critical values
        in percents.  The function returns critical values for a
        differing set of significance levels depending on the
        distribution that is being tested against.

    Notes
    -----
    Critical values provided are for the following significance levels:

    normal/exponenential
        15%, 10%, 5%, 2.5%, 1%
    logistic
        25%, 10%, 5%, 2.5%, 1%, 0.5%
    Gumbel
        25%, 10%, 5%, 2.5%, 1%

    If A2 is larger than these critical values then for the corresponding
    significance level, the null hypothesis that the data come from the
    chosen distribution can be rejected.

    References
    ----------
    .. [1] http://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm
    .. [2] Stephens, M. A. (1974). EDF Statistics for Goodness of Fit and
           Some Comparisons, Journal of the American Statistical Association,
           Vol. 69, pp. 730-737.
    .. [3] Stephens, M. A. (1976). Asymptotic Results for Goodness-of-Fit
           Statistics with Unknown Parameters, Annals of Statistics, Vol. 4,
           pp. 357-369.
    .. [4] Stephens, M. A. (1977). Goodness of Fit for the Extreme Value
           Distribution, Biometrika, Vol. 64, pp. 583-588.
    .. [5] Stephens, M. A. (1977). Goodness of Fit with Special Reference
           to Tests for Exponentiality , Technical Report No. 262,
           Department of Statistics, Stanford University, Stanford, CA.
    .. [6] Stephens, M. A. (1979). Tests of Fit for the Logistic Distribution
           Based on the Empirical Distribution Function, Biometrika, Vol. 66,
           pp. 591-595.

    """
    if dist not in ['norm', 'expon', 'gumbel', 'extreme1', 'logistic']:
        raise ValueError("Invalid distribution; dist must be 'norm', "
                         "'expon', 'gumbel', 'extreme1' or 'logistic'.")
    y = sort(x)
    xbar = np.mean(x, axis=0)
    N = len(y)
    if dist == 'norm':
        s = np.std(x, ddof=1, axis=0)
        w = (y - xbar) / s
        z = distributions.norm.cdf(w)
        sig = array([15, 10, 5, 2.5, 1])
        critical = around(_Avals_norm / (1.0 + 4.0/N - 25.0/N/N), 3)
    elif dist == 'expon':
        w = y / xbar
        z = distributions.expon.cdf(w)
        sig = array([15, 10, 5, 2.5, 1])
        critical = around(_Avals_expon / (1.0 + 0.6/N), 3)
    elif dist == 'logistic':
        def rootfunc(ab, xj, N):
            a, b = ab
            tmp = (xj - a) / b
            tmp2 = exp(tmp)
            val = [sum(1.0/(1+tmp2), axis=0) - 0.5*N,
                   sum(tmp*(1.0-tmp2)/(1+tmp2), axis=0) + N]
            return array(val)

        sol0 = array([xbar, np.std(x, ddof=1, axis=0)])
        sol = optimize.fsolve(rootfunc, sol0, args=(x, N), xtol=1e-5)
        w = (y - sol[0]) / sol[1]
        z = distributions.logistic.cdf(w)
        sig = array([25, 10, 5, 2.5, 1, 0.5])
        critical = around(_Avals_logistic / (1.0 + 0.25/N), 3)
    else:  # (dist == 'gumbel') or (dist == 'extreme1'):
        xbar, s = distributions.gumbel_l.fit(x)
        w = (y - xbar) / s
        z = distributions.gumbel_l.cdf(w)
        sig = array([25, 10, 5, 2.5, 1])
        critical = around(_Avals_gumbel / (1.0 + 0.2/sqrt(N)), 3)

    i = arange(1, N + 1)
    A2 = -N - sum((2*i - 1.0) / N * (log(z) + log(1 - z[::-1])), axis=0)

    return AndersonResult(A2, critical, sig)


def _anderson_ksamp_midrank(samples, Z, Zstar, k, n, N):
    """
    Compute A2akN equation 7 of Scholz and Stephens.

    Parameters
    ----------
    samples : sequence of 1-D array_like
        Array of sample arrays.
    Z : array_like
        Sorted array of all observations.
    Zstar : array_like
        Sorted array of unique observations.
    k : int
        Number of samples.
    n : array_like
        Number of observations in each sample.
    N : int
        Total number of observations.

    Returns
    -------
    A2aKN : float
        The A2aKN statistics of Scholz and Stephens 1987.
    """

    A2akN = 0.
    Z_ssorted_left = Z.searchsorted(Zstar, 'left')
    if N == Zstar.size:
        lj = 1.
    else:
        lj = Z.searchsorted(Zstar, 'right') - Z_ssorted_left
    Bj = Z_ssorted_left + lj / 2.
    for i in arange(0, k):
        s = np.sort(samples[i])
        s_ssorted_right = s.searchsorted(Zstar, side='right')
        Mij = s_ssorted_right.astype(np.float)
        fij = s_ssorted_right - s.searchsorted(Zstar, 'left')
        Mij -= fij / 2.
        inner = lj / float(N) * (N*Mij - Bj*n[i])**2 / (Bj*(N - Bj) - N*lj/4.)
        A2akN += inner.sum() / n[i]
    A2akN *= (N - 1.) / N
    return A2akN


def _anderson_ksamp_right(samples, Z, Zstar, k, n, N):
    """
    Compute A2akN equation 6 of Scholz & Stephens.

    Parameters
    ----------
    samples : sequence of 1-D array_like
        Array of sample arrays.
    Z : array_like
        Sorted array of all observations.
    Zstar : array_like
        Sorted array of unique observations.
    k : int
        Number of samples.
    n : array_like
        Number of observations in each sample.
    N : int
        Total number of observations.

    Returns
    -------
    A2KN : float
        The A2KN statistics of Scholz and Stephens 1987.
    """

    A2kN = 0.
    lj = Z.searchsorted(Zstar[:-1], 'right') - Z.searchsorted(Zstar[:-1],
                                                              'left')
    Bj = lj.cumsum()
    for i in arange(0, k):
        s = np.sort(samples[i])
        Mij = s.searchsorted(Zstar[:-1], side='right')
        inner = lj / float(N) * (N * Mij - Bj * n[i])**2 / (Bj * (N - Bj))
        A2kN += inner.sum() / n[i]
    return A2kN


Anderson_ksampResult = namedtuple('Anderson_ksampResult',
                                  ('statistic', 'critical_values',
                                   'significance_level'))


def anderson_ksamp(samples, midrank=True):
    """The Anderson-Darling test for k-samples.

    The k-sample Anderson-Darling test is a modification of the
    one-sample Anderson-Darling test. It tests the null hypothesis
    that k-samples are drawn from the same population without having
    to specify the distribution function of that population. The
    critical values depend on the number of samples.

    Parameters
    ----------
    samples : sequence of 1-D array_like
        Array of sample data in arrays.
    midrank : bool, optional
        Type of Anderson-Darling test which is computed. Default
        (True) is the midrank test applicable to continuous and
        discrete populations. If False, the right side empirical
        distribution is used.

    Returns
    -------
    statistic : float
        Normalized k-sample Anderson-Darling test statistic.
    critical_values : array
        The critical values for significance levels 25%, 10%, 5%, 2.5%, 1%.
    significance_level : float
        An approximate significance level at which the null hypothesis for the
        provided samples can be rejected.

    Raises
    ------
    ValueError
        If less than 2 samples are provided, a sample is empty, or no
        distinct observations are in the samples.

    See Also
    --------
    ks_2samp : 2 sample Kolmogorov-Smirnov test
    anderson : 1 sample Anderson-Darling test

    Notes
    -----
    [1]_ Defines three versions of the k-sample Anderson-Darling test:
    one for continuous distributions and two for discrete
    distributions, in which ties between samples may occur. The
    default of this routine is to compute the version based on the
    midrank empirical distribution function. This test is applicable
    to continuous and discrete data. If midrank is set to False, the
    right side empirical distribution is used for a test for discrete
    data. According to [1]_, the two discrete test statistics differ
    only slightly if a few collisions due to round-off errors occur in
    the test not adjusted for ties between samples.

    .. versionadded:: 0.14.0

    References
    ----------
    .. [1] Scholz, F. W and Stephens, M. A. (1987), K-Sample
           Anderson-Darling Tests, Journal of the American Statistical
           Association, Vol. 82, pp. 918-924.

    Examples
    --------
    >>> from scipy import stats
    >>> np.random.seed(314159)

    The null hypothesis that the two random samples come from the same
    distribution can be rejected at the 5% level because the returned
    test value is greater than the critical value for 5% (1.961) but
    not at the 2.5% level. The interpolation gives an approximate
    significance level of 3.1%:

    >>> stats.anderson_ksamp([np.random.normal(size=50),
    ... np.random.normal(loc=0.5, size=30)])
    (2.4615796189876105,
      array([ 0.325,  1.226,  1.961,  2.718,  3.752]),
      0.03134990135800783)


    The null hypothesis cannot be rejected for three samples from an
    identical distribution. The approximate p-value (87%) has to be
    computed by extrapolation and may not be very accurate:

    >>> stats.anderson_ksamp([np.random.normal(size=50),
    ... np.random.normal(size=30), np.random.normal(size=20)])
    (-0.73091722665244196,
      array([ 0.44925884,  1.3052767 ,  1.9434184 ,  2.57696569,  3.41634856]),
      0.8789283903979661)

    """
    k = len(samples)
    if (k < 2):
        raise ValueError("anderson_ksamp needs at least two samples")

    samples = list(map(np.asarray, samples))
    Z = np.sort(np.hstack(samples))
    N = Z.size
    Zstar = np.unique(Z)
    if Zstar.size < 2:
        raise ValueError("anderson_ksamp needs more than one distinct "
                         "observation")

    n = np.array([sample.size for sample in samples])
    if any(n == 0):
        raise ValueError("anderson_ksamp encountered sample without "
                         "observations")

    if midrank:
        A2kN = _anderson_ksamp_midrank(samples, Z, Zstar, k, n, N)
    else:
        A2kN = _anderson_ksamp_right(samples, Z, Zstar, k, n, N)

    H = (1. / n).sum()
    hs_cs = (1. / arange(N - 1, 1, -1)).cumsum()
    h = hs_cs[-1] + 1
    g = (hs_cs / arange(2, N)).sum()

    a = (4*g - 6) * (k - 1) + (10 - 6*g)*H
    b = (2*g - 4)*k**2 + 8*h*k + (2*g - 14*h - 4)*H - 8*h + 4*g - 6
    c = (6*h + 2*g - 2)*k**2 + (4*h - 4*g + 6)*k + (2*h - 6)*H + 4*h
    d = (2*h + 6)*k**2 - 4*h*k
    sigmasq = (a*N**3 + b*N**2 + c*N + d) / ((N - 1.) * (N - 2.) * (N - 3.))
    m = k - 1
    A2 = (A2kN - m) / math.sqrt(sigmasq)

    # The b_i values are the interpolation coefficients from Table 2
    # of Scholz and Stephens 1987
    b0 = np.array([0.675, 1.281, 1.645, 1.96, 2.326])
    b1 = np.array([-0.245, 0.25, 0.678, 1.149, 1.822])
    b2 = np.array([-0.105, -0.305, -0.362, -0.391, -0.396])
    critical = b0 + b1 / math.sqrt(m) + b2 / m
    pf = np.polyfit(critical, log(np.array([0.25, 0.1, 0.05, 0.025, 0.01])), 2)
    if A2 < critical.min() or A2 > critical.max():
        warnings.warn("approximate p-value will be computed by extrapolation")

    p = math.exp(np.polyval(pf, A2))

    return Anderson_ksampResult(A2, critical, p)


AnsariResult = namedtuple('AnsariResult', ('statistic', 'pvalue'))


def ansari(x, y):
    """
    Perform the Ansari-Bradley test for equal scale parameters

    The Ansari-Bradley test is a non-parametric test for the equality
    of the scale parameter of the distributions from which two
    samples were drawn.

    Parameters
    ----------
    x, y : array_like
        arrays of sample data

    Returns
    -------
    statistic : float
        The Ansari-Bradley test statistic
    pvalue : float
        The p-value of the hypothesis test

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    mood : A non-parametric test for the equality of two scale parameters

    Notes
    -----
    The p-value given is exact when the sample sizes are both less than
    55 and there are no ties, otherwise a normal approximation for the
    p-value is used.

    References
    ----------
    .. [1] Sprent, Peter and N.C. Smeeton.  Applied nonparametric statistical
           methods.  3rd ed. Chapman and Hall/CRC. 2001.  Section 5.8.2.

    """
    x, y = asarray(x), asarray(y)
    n = len(x)
    m = len(y)
    if m < 1:
        raise ValueError("Not enough other observations.")
    if n < 1:
        raise ValueError("Not enough test observations.")

    N = m + n
    xy = r_[x, y]  # combine
    rank = stats.rankdata(xy)
    symrank = amin(array((rank, N - rank + 1)), 0)
    AB = sum(symrank[:n], axis=0)
    uxy = unique(xy)
    repeats = (len(uxy) != len(xy))
    exact = ((m < 55) and (n < 55) and not repeats)
    if repeats and (m < 55 or n < 55):
        warnings.warn("Ties preclude use of exact statistic.")
    if exact:
        astart, a1, ifault = statlib.gscale(n, m)
        ind = AB - astart
        total = sum(a1, axis=0)
        if ind < len(a1)/2.0:
            cind = int(ceil(ind))
            if ind == cind:
                pval = 2.0 * sum(a1[:cind+1], axis=0) / total
            else:
                pval = 2.0 * sum(a1[:cind], axis=0) / total
        else:
            find = int(floor(ind))
            if ind == floor(ind):
                pval = 2.0 * sum(a1[find:], axis=0) / total
            else:
                pval = 2.0 * sum(a1[find+1:], axis=0) / total
        return AnsariResult(AB, min(1.0, pval))

    # otherwise compute normal approximation
    if N % 2:  # N odd
        mnAB = n * (N+1.0)**2 / 4.0 / N
        varAB = n * m * (N+1.0) * (3+N**2) / (48.0 * N**2)
    else:
        mnAB = n * (N+2.0) / 4.0
        varAB = m * n * (N+2) * (N-2.0) / 48 / (N-1.0)
    if repeats:   # adjust variance estimates
        # compute sum(tj * rj**2,axis=0)
        fac = sum(symrank**2, axis=0)
        if N % 2:  # N odd
            varAB = m * n * (16*N*fac - (N+1)**4) / (16.0 * N**2 * (N-1))
        else:  # N even
            varAB = m * n * (16*fac - N*(N+2)**2) / (16.0 * N * (N-1))

    z = (AB - mnAB) / sqrt(varAB)
    pval = distributions.norm.sf(abs(z)) * 2.0
    return AnsariResult(AB, pval)


BartlettResult = namedtuple('BartlettResult', ('statistic', 'pvalue'))


def bartlett(*args):
    """
    Perform Bartlett's test for equal variances

    Bartlett's test tests the null hypothesis that all input samples
    are from populations with equal variances.  For samples
    from significantly non-normal populations, Levene's test
    `levene` is more robust.

    Parameters
    ----------
    sample1, sample2,... : array_like
        arrays of sample data.  May be different lengths.

    Returns
    -------
    statistic : float
        The test statistic.
    pvalue : float
        The p-value of the test.

    References
    ----------
    .. [1]  http://www.itl.nist.gov/div898/handbook/eda/section3/eda357.htm

    .. [2]  Snedecor, George W. and Cochran, William G. (1989), Statistical
              Methods, Eighth Edition, Iowa State University Press.

    """
    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    Ni = zeros(k)
    ssq = zeros(k, 'd')
    for j in range(k):
        Ni[j] = len(args[j])
        ssq[j] = np.var(args[j], ddof=1)
    Ntot = sum(Ni, axis=0)
    spsq = sum((Ni - 1)*ssq, axis=0) / (1.0*(Ntot - k))
    numer = (Ntot*1.0 - k) * log(spsq) - sum((Ni - 1.0)*log(ssq), axis=0)
    denom = 1.0 + 1.0/(3*(k - 1)) * ((sum(1.0/(Ni - 1.0), axis=0)) -
                                     1.0/(Ntot - k))
    T = numer / denom
    pval = distributions.chi2.sf(T, k - 1)  # 1 - cdf

    return BartlettResult(T, pval)


LeveneResult = namedtuple('LeveneResult', ('statistic', 'pvalue'))


def levene(*args, **kwds):
    """
    Perform Levene test for equal variances.

    The Levene test tests the null hypothesis that all input samples
    are from populations with equal variances.  Levene's test is an
    alternative to Bartlett's test `bartlett` in the case where
    there are significant deviations from normality.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        The sample data, possibly with different lengths
    center : {'mean', 'median', 'trimmed'}, optional
        Which function of the data to use in the test.  The default
        is 'median'.
    proportiontocut : float, optional
        When `center` is 'trimmed', this gives the proportion of data points
        to cut from each end. (See `scipy.stats.trim_mean`.)
        Default is 0.05.

    Returns
    -------
    statistic : float
        The test statistic.
    pvalue : float
        The p-value for the test.

    Notes
    -----
    Three variations of Levene's test are possible.  The possibilities
    and their recommended usages are:

      * 'median' : Recommended for skewed (non-normal) distributions>
      * 'mean' : Recommended for symmetric, moderate-tailed distributions.
      * 'trimmed' : Recommended for heavy-tailed distributions.

    References
    ----------
    .. [1]  http://www.itl.nist.gov/div898/handbook/eda/section3/eda35a.htm
    .. [2]   Levene, H. (1960). In Contributions to Probability and Statistics:
               Essays in Honor of Harold Hotelling, I. Olkin et al. eds.,
               Stanford University Press, pp. 278-292.
    .. [3]  Brown, M. B. and Forsythe, A. B. (1974), Journal of the American
              Statistical Association, 69, 364-367

    """
    # Handle keyword arguments.
    center = 'median'
    proportiontocut = 0.05
    for kw, value in kwds.items():
        if kw not in ['center', 'proportiontocut']:
            raise TypeError("levene() got an unexpected keyword "
                            "argument '%s'" % kw)
        if kw == 'center':
            center = value
        else:
            proportiontocut = value

    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")
    Ni = zeros(k)
    Yci = zeros(k, 'd')

    if center not in ['mean', 'median', 'trimmed']:
        raise ValueError("Keyword argument <center> must be 'mean', 'median'"
                         + "or 'trimmed'.")

    if center == 'median':
        func = lambda x: np.median(x, axis=0)
    elif center == 'mean':
        func = lambda x: np.mean(x, axis=0)
    else:  # center == 'trimmed'
        args = tuple(stats.trimboth(np.sort(arg), proportiontocut)
                     for arg in args)
        func = lambda x: np.mean(x, axis=0)

    for j in range(k):
        Ni[j] = len(args[j])
        Yci[j] = func(args[j])
    Ntot = sum(Ni, axis=0)

    # compute Zij's
    Zij = [None] * k
    for i in range(k):
        Zij[i] = abs(asarray(args[i]) - Yci[i])

    # compute Zbari
    Zbari = zeros(k, 'd')
    Zbar = 0.0
    for i in range(k):
        Zbari[i] = np.mean(Zij[i], axis=0)
        Zbar += Zbari[i] * Ni[i]

    Zbar /= Ntot
    numer = (Ntot - k) * sum(Ni * (Zbari - Zbar)**2, axis=0)

    # compute denom_variance
    dvar = 0.0
    for i in range(k):
        dvar += sum((Zij[i] - Zbari[i])**2, axis=0)

    denom = (k - 1.0) * dvar

    W = numer / denom
    pval = distributions.f.sf(W, k-1, Ntot-k)  # 1 - cdf

    return LeveneResult(W, pval)


@setastest(False)
def binom_test(x, n=None, p=0.5):
    """
    Perform a test that the probability of success is p.

    This is an exact, two-sided test of the null hypothesis
    that the probability of success in a Bernoulli experiment
    is `p`.

    Parameters
    ----------
    x : integer or array_like
        the number of successes, or if x has length 2, it is the
        number of successes and the number of failures.
    n : integer
        the number of trials.  This is ignored if x gives both the
        number of successes and failures
    p : float, optional
        The hypothesized probability of success.  0 <= p <= 1. The
        default value is p = 0.5

    Returns
    -------
    p-value : float
        The p-value of the hypothesis test

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Binomial_test

    """
    x = atleast_1d(x).astype(np.integer)
    if len(x) == 2:
        n = x[1] + x[0]
        x = x[0]
    elif len(x) == 1:
        x = x[0]
        if n is None or n < x:
            raise ValueError("n must be >= x")
        n = np.int_(n)
    else:
        raise ValueError("Incorrect length for x.")

    if (p > 1.0) or (p < 0.0):
        raise ValueError("p must be in range [0,1]")

    d = distributions.binom.pmf(x, n, p)
    rerr = 1 + 1e-7
    if x == p * n:
        # special case as shortcut, would also be handled by `else` below
        pval = 1.
    elif x < p * n:
        i = np.arange(np.ceil(p * n), n+1)
        y = np.sum(distributions.binom.pmf(i, n, p) <= d*rerr, axis=0)
        pval = (distributions.binom.cdf(x, n, p) +
                distributions.binom.sf(n - y, n, p))
    else:
        i = np.arange(np.floor(p*n) + 1)
        y = np.sum(distributions.binom.pmf(i, n, p) <= d*rerr, axis=0)
        pval = (distributions.binom.cdf(y-1, n, p) +
                distributions.binom.sf(x-1, n, p))

    return min(1.0, pval)


def _apply_func(x, g, func):
    # g is list of indices into x
    #  separating x into different groups
    #  func should be applied over the groups
    g = unique(r_[0, g, len(x)])
    output = []
    for k in range(len(g) - 1):
        output.append(func(x[g[k]:g[k+1]]))

    return asarray(output)


def fligner(*args, **kwds):
    """
    Perform Fligner's test for equal variances.

    Fligner's test tests the null hypothesis that all input samples
    are from populations with equal variances.  Fligner's test is
    non-parametric in contrast to Bartlett's test `bartlett` and
    Levene's test `levene`.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        Arrays of sample data.  Need not be the same length.
    center : {'mean', 'median', 'trimmed'}, optional
        Keyword argument controlling which function of the data is used in
        computing the test statistic.  The default is 'median'.
    proportiontocut : float, optional
        When `center` is 'trimmed', this gives the proportion of data points
        to cut from each end. (See `scipy.stats.trim_mean`.)
        Default is 0.05.

    Returns
    -------
    Xsq : float
        The test statistic.
    p-value : float
        The p-value for the hypothesis test.

    Notes
    -----
    As with Levene's test there are three variants of Fligner's test that
    differ by the measure of central tendency used in the test.  See `levene`
    for more information.

    References
    ----------
    .. [1] http://www.stat.psu.edu/~bgl/center/tr/TR993.ps

    .. [2] Fligner, M.A. and Killeen, T.J. (1976). Distribution-free two-sample
           tests for scale. 'Journal of the American Statistical Association.'
           71(353), 210-213.

    """
    # Handle keyword arguments.
    center = 'median'
    proportiontocut = 0.05
    for kw, value in kwds.items():
        if kw not in ['center', 'proportiontocut']:
            raise TypeError("fligner() got an unexpected keyword "
                            "argument '%s'" % kw)
        if kw == 'center':
            center = value
        else:
            proportiontocut = value

    k = len(args)
    if k < 2:
        raise ValueError("Must enter at least two input sample vectors.")

    if center not in ['mean', 'median', 'trimmed']:
        raise ValueError("Keyword argument <center> must be 'mean', 'median'"
                         + "or 'trimmed'.")

    if center == 'median':
        func = lambda x: np.median(x, axis=0)
    elif center == 'mean':
        func = lambda x: np.mean(x, axis=0)
    else:  # center == 'trimmed'
        args = tuple(stats.trimboth(arg, proportiontocut) for arg in args)
        func = lambda x: np.mean(x, axis=0)

    Ni = asarray([len(args[j]) for j in range(k)])
    Yci = asarray([func(args[j]) for j in range(k)])
    Ntot = sum(Ni, axis=0)
    # compute Zij's
    Zij = [abs(asarray(args[i]) - Yci[i]) for i in range(k)]
    allZij = []
    g = [0]
    for i in range(k):
        allZij.extend(list(Zij[i]))
        g.append(len(allZij))

    ranks = stats.rankdata(allZij)
    a = distributions.norm.ppf(ranks / (2*(Ntot + 1.0)) + 0.5)

    # compute Aibar
    Aibar = _apply_func(a, g, sum) / Ni
    anbar = np.mean(a, axis=0)
    varsq = np.var(a, axis=0, ddof=1)
    Xsq = sum(Ni * (asarray(Aibar) - anbar)**2.0, axis=0) / varsq
    pval = distributions.chi2.sf(Xsq, k - 1)  # 1 - cdf
    return Xsq, pval


def mood(x, y, axis=0):
    """
    Perform Mood's test for equal scale parameters.

    Mood's two-sample test for scale parameters is a non-parametric
    test for the null hypothesis that two samples are drawn from the
    same distribution with the same scale parameter.

    Parameters
    ----------
    x, y : array_like
        Arrays of sample data.
    axis : int, optional
        The axis along which the samples are tested.  `x` and `y` can be of
        different length along `axis`.
        If `axis` is None, `x` and `y` are flattened and the test is done on
        all values in the flattened arrays.

    Returns
    -------
    z : scalar or ndarray
        The z-score for the hypothesis test.  For 1-D inputs a scalar is
        returned.
    p-value : scalar ndarray
        The p-value for the hypothesis test.

    See Also
    --------
    fligner : A non-parametric test for the equality of k variances
    ansari : A non-parametric test for the equality of 2 variances
    bartlett : A parametric test for equality of k variances in normal samples
    levene : A parametric test for equality of k variances

    Notes
    -----
    The data are assumed to be drawn from probability distributions ``f(x)``
    and ``f(x/s) / s`` respectively, for some probability density function f.
    The null hypothesis is that ``s == 1``.

    For multi-dimensional arrays, if the inputs are of shapes
    ``(n0, n1, n2, n3)``  and ``(n0, m1, n2, n3)``, then if ``axis=1``, the
    resulting z and p values will have shape ``(n0, n2, n3)``.  Note that
    ``n1`` and ``m1`` don't have to be equal, but the other dimensions do.

    Examples
    --------
    >>> from scipy import stats
    >>> x2 = np.random.randn(2, 45, 6, 7)
    >>> x1 = np.random.randn(2, 30, 6, 7)
    >>> z, p = stats.mood(x1, x2, axis=1)
    >>> p.shape
    (2, 6, 7)

    Find the number of points where the difference in scale is not significant:

    >>> (p > 0.1).sum()
    74

    Perform the test with different scales:

    >>> x1 = np.random.randn(2, 30)
    >>> x2 = np.random.randn(2, 35) * 10.0
    >>> stats.mood(x1, x2, axis=1)
    (array([-5.84332354, -5.6840814 ]), array([5.11694980e-09, 1.31517628e-08]))

    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if axis is None:
        x = x.flatten()
        y = y.flatten()
        axis = 0

    # Determine shape of the result arrays
    res_shape = tuple([x.shape[ax] for ax in range(len(x.shape)) if ax != axis])
    if not (res_shape == tuple([y.shape[ax] for ax in range(len(y.shape)) if
                                ax != axis])):
        raise ValueError("Dimensions of x and y on all axes except `axis` "
                         "should match")

    n = x.shape[axis]
    m = y.shape[axis]
    N = m + n
    if N < 3:
        raise ValueError("Not enough observations.")

    xy = np.concatenate((x, y), axis=axis)
    if axis != 0:
        xy = np.rollaxis(xy, axis)

    xy = xy.reshape(xy.shape[0], -1)

    # Generalized to the n-dimensional case by adding the axis argument, and
    # using for loops, since rankdata is not vectorized.  For improving
    # performance consider vectorizing rankdata function.
    all_ranks = np.zeros_like(xy)
    for j in range(xy.shape[1]):
        all_ranks[:, j] = stats.rankdata(xy[:, j])

    Ri = all_ranks[:n]
    M = sum((Ri - (N + 1.0) / 2)**2, axis=0)
    # Approx stat.
    mnM = n * (N * N - 1.0) / 12
    varM = m * n * (N + 1.0) * (N + 2) * (N - 2) / 180
    z = (M - mnM) / sqrt(varM)

    # sf for right tail, cdf for left tail.  Factor 2 for two-sidedness
    z_pos = z > 0
    pval = np.zeros_like(z)
    pval[z_pos] = 2 * distributions.norm.sf(z[z_pos])
    pval[~z_pos] = 2 * distributions.norm.cdf(z[~z_pos])

    if res_shape == ():
        # Return scalars, not 0-D arrays
        z = z[0]
        pval = pval[0]
    else:
        z.shape = res_shape
        pval.shape = res_shape

    return z, pval


WilcoxonResult = namedtuple('WilcoxonResult', ('statistic', 'pvalue'))


def wilcoxon(x, y=None, zero_method="wilcox", correction=False):
    """
    Calculate the Wilcoxon signed-rank test.

    The Wilcoxon signed-rank test tests the null hypothesis that two
    related paired samples come from the same distribution. In particular,
    it tests whether the distribution of the differences x - y is symmetric
    about zero. It is a non-parametric version of the paired T-test.

    Parameters
    ----------
    x : array_like
        The first set of measurements.
    y : array_like, optional
        The second set of measurements.  If `y` is not given, then the `x`
        array is considered to be the differences between the two sets of
        measurements.
    zero_method : string, {"pratt", "wilcox", "zsplit"}, optional
        "pratt":
            Pratt treatment: includes zero-differences in the ranking process
            (more conservative)
        "wilcox":
            Wilcox treatment: discards all zero-differences
        "zsplit":
            Zero rank split: just like Pratt, but spliting the zero rank
            between positive and negative ones
    correction : bool, optional
        If True, apply continuity correction by adjusting the Wilcoxon rank
        statistic by 0.5 towards the mean value when computing the
        z-statistic.  Default is False.

    Returns
    -------
    statistic : float
        The sum of the ranks of the differences above or below zero, whichever
        is smaller.
    pvalue : float
        The two-sided p-value for the test.

    Notes
    -----
    Because the normal approximation is used for the calculations, the
    samples used should be large.  A typical rule is to require that
    n > 20.

    References
    ----------
    .. [1] http://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test

    """

    if zero_method not in ["wilcox", "pratt", "zsplit"]:
        raise ValueError("Zero method should be either 'wilcox' "
                         "or 'pratt' or 'zsplit'")

    if y is None:
        d = x
    else:
        x, y = map(asarray, (x, y))
        if len(x) != len(y):
            raise ValueError('Unequal N in wilcoxon.  Aborting.')
        d = x - y

    if zero_method == "wilcox":
        # Keep all non-zero differences
        d = compress(np.not_equal(d, 0), d, axis=-1)

    count = len(d)
    if count < 10:
        warnings.warn("Warning: sample size too small for normal approximation.")
    r = stats.rankdata(abs(d))
    r_plus = sum((d > 0) * r, axis=0)
    r_minus = sum((d < 0) * r, axis=0)

    if zero_method == "zsplit":
        r_zero = sum((d == 0) * r, axis=0)
        r_plus += r_zero / 2.
        r_minus += r_zero / 2.

    T = min(r_plus, r_minus)
    mn = count * (count + 1.) * 0.25
    se = count * (count + 1.) * (2. * count + 1.)

    if zero_method == "pratt":
        r = r[d != 0]

    replist, repnum = find_repeats(r)
    if repnum.size != 0:
        # Correction for repeated elements.
        se -= 0.5 * (repnum * (repnum * repnum - 1)).sum()

    se = sqrt(se / 24)
    correction = 0.5 * int(bool(correction)) * np.sign(T - mn)
    z = (T - mn - correction) / se
    prob = 2. * distributions.norm.sf(abs(z))

    return WilcoxonResult(T, prob)


@setastest(False)
def median_test(*args, **kwds):
    """
    Mood's median test.

    Test that two or more samples come from populations with the same median.

    Let ``n = len(args)`` be the number of samples.  The "grand median" of
    all the data is computed, and a contingency table is formed by
    classifying the values in each sample as being above or below the grand
    median.  The contingency table, along with `correction` and `lambda_`,
    are passed to `scipy.stats.chi2_contingency` to compute the test statistic
    and p-value.

    Parameters
    ----------
    sample1, sample2, ... : array_like
        The set of samples.  There must be at least two samples.
        Each sample must be a one-dimensional sequence containing at least
        one value.  The samples are not required to have the same length.
    ties : str, optional
        Determines how values equal to the grand median are classified in
        the contingency table.  The string must be one of::

            "below":
                Values equal to the grand median are counted as "below".
            "above":
                Values equal to the grand median are counted as "above".
            "ignore":
                Values equal to the grand median are not counted.

        The default is "below".
    correction : bool, optional
        If True, *and* there are just two samples, apply Yates' correction
        for continuity when computing the test statistic associated with
        the contingency table.  Default is True.
    lambda_ : float or str, optional.
        By default, the statistic computed in this test is Pearson's
        chi-squared statistic.  `lambda_` allows a statistic from the
        Cressie-Read power divergence family to be used instead.  See
        `power_divergence` for details.
        Default is 1 (Pearson's chi-squared statistic).

    Returns
    -------
    stat : float
        The test statistic.  The statistic that is returned is determined by
        `lambda_`.  The default is Pearson's chi-squared statistic.
    p : float
        The p-value of the test.
    m : float
        The grand median.
    table : ndarray
        The contingency table.  The shape of the table is (2, n), where
        n is the number of samples.  The first row holds the counts of the
        values above the grand median, and the second row holds the counts
        of the values below the grand median.  The table allows further
        analysis with, for example, `scipy.stats.chi2_contingency`, or with
        `scipy.stats.fisher_exact` if there are two samples, without having
        to recompute the table.

    See Also
    --------
    kruskal : Compute the Kruskal-Wallis H-test for independent samples.
    mannwhitneyu : Computes the Mann-Whitney rank test on samples x and y.

    Notes
    -----
    .. versionadded:: 0.15.0

    References
    ----------
    .. [1] Mood, A. M., Introduction to the Theory of Statistics. McGraw-Hill
        (1950), pp. 394-399.
    .. [2] Zar, J. H., Biostatistical Analysis, 5th ed. Prentice Hall (2010).
        See Sections 8.12 and 10.15.

    Examples
    --------
    A biologist runs an experiment in which there are three groups of plants.
    Group 1 has 16 plants, group 2 has 15 plants, and group 3 has 17 plants.
    Each plant produces a number of seeds.  The seed counts for each group
    are::

        Group 1: 10 14 14 18 20 22 24 25 31 31 32 39 43 43 48 49
        Group 2: 28 30 31 33 34 35 36 40 44 55 57 61 91 92 99
        Group 3:  0  3  9 22 23 25 25 33 34 34 40 45 46 48 62 67 84

    The following code applies Mood's median test to these samples.

    >>> g1 = [10, 14, 14, 18, 20, 22, 24, 25, 31, 31, 32, 39, 43, 43, 48, 49]
    >>> g2 = [28, 30, 31, 33, 34, 35, 36, 40, 44, 55, 57, 61, 91, 92, 99]
    >>> g3 = [0, 3, 9, 22, 23, 25, 25, 33, 34, 34, 40, 45, 46, 48, 62, 67, 84]
    >>> from scipy.stats import median_test
    >>> stat, p, med, tbl = median_test(g1, g2, g3)

    The median is

    >>> med
    34.0

    and the contingency table is

    >>> tbl
    array([[ 5, 10,  7],
           [11,  5, 10]])

    `p` is too large to conclude that the medians are not the same:

    >>> p
    0.12609082774093244

    The "G-test" can be performed by passing ``lambda_="log-likelihood"`` to
    `median_test`.

    >>> g, p, med, tbl = median_test(g1, g2, g3, lambda_="log-likelihood")
    >>> p
    0.12224779737117837

    The median occurs several times in the data, so we'll get a different
    result if, for example, ``ties="above"`` is used:

    >>> stat, p, med, tbl = median_test(g1, g2, g3, ties="above")
    >>> p
    0.063873276069553273

    >>> tbl
    array([[ 5, 11,  9],
           [11,  4,  8]])

    This example demonstrates that if the data set is not large and there
    are values equal to the median, the p-value can be sensitive to the
    choice of `ties`.

    """
    ties = kwds.pop('ties', 'below')
    correction = kwds.pop('correction', True)
    lambda_ = kwds.pop('lambda_', None)

    if len(kwds) > 0:
        bad_kwd = kwds.keys()[0]
        raise TypeError("median_test() got an unexpected keyword "
                        "argument %r" % bad_kwd)

    if len(args) < 2:
        raise ValueError('median_test requires two or more samples.')

    ties_options = ['below', 'above', 'ignore']
    if ties not in ties_options:
        raise ValueError("invalid 'ties' option '%s'; 'ties' must be one "
                         "of: %s" % (ties, str(ties_options)[1:-1]))

    data = [np.asarray(arg) for arg in args]

    # Validate the sizes and shapes of the arguments.
    for k, d in enumerate(data):
        if d.size == 0:
            raise ValueError("Sample %d is empty. All samples must "
                             "contain at least one value." % (k + 1))
        if d.ndim != 1:
            raise ValueError("Sample %d has %d dimensions.  All "
                             "samples must be one-dimensional sequences." %
                             (k + 1, d.ndim))

    grand_median = np.median(np.concatenate(data))

    # Create the contingency table.
    table = np.zeros((2, len(data)), dtype=np.int64)
    for k, sample in enumerate(data):
        nabove = count_nonzero(sample > grand_median)
        nbelow = count_nonzero(sample < grand_median)
        nequal = sample.size - (nabove + nbelow)
        table[0, k] += nabove
        table[1, k] += nbelow
        if ties == "below":
            table[1, k] += nequal
        elif ties == "above":
            table[0, k] += nequal

    # Check that no row or column of the table is all zero.
    # Such a table can not be given to chi2_contingency, because it would have
    # a zero in the table of expected frequencies.
    rowsums = table.sum(axis=1)
    if rowsums[0] == 0:
        raise ValueError("All values are below the grand median (%r)." %
                         grand_median)
    if rowsums[1] == 0:
        raise ValueError("All values are above the grand median (%r)." %
                         grand_median)
    if ties == "ignore":
        # We already checked that each sample has at least one value, but it
        # is possible that all those values equal the grand median.  If `ties`
        # is "ignore", that would result in a column of zeros in `table`.  We
        # check for that case here.
        zero_cols = np.where((table == 0).all(axis=0))[0]
        if len(zero_cols) > 0:
            msg = ("All values in sample %d are equal to the grand "
                   "median (%r), so they are ignored, resulting in an "
                   "empty sample." % (zero_cols[0] + 1, grand_median))
            raise ValueError(msg)

    stat, p, dof, expected = chi2_contingency(table, lambda_=lambda_,
                                              correction=correction)
    return stat, p, grand_median, table


def _hermnorm(N):
    # return the negatively normalized hermite polynomials up to order N-1
    #  (inclusive)
    #  using the recursive relationship
    #  p_n+1 = p_n(x)' - x*p_n(x)
    #   and p_0(x) = 1
    plist = [None] * N
    plist[0] = poly1d(1)
    for n in range(1, N):
        plist[n] = plist[n-1].deriv() - poly1d([1, 0]) * plist[n-1]

    return plist


# Note: when removing pdf_fromgamma, also remove the _hermnorm support function
@np.deprecate(message="scipy.stats.pdf_fromgamma is deprecated in scipy 0.16.0 "
                      "in favour of statsmodels.distributions.ExpandedNormal.")
def pdf_fromgamma(g1, g2, g3=0.0, g4=None):
    if g4 is None:
        g4 = 3 * g2**2
    sigsq = 1.0 / g2
    sig = sqrt(sigsq)
    mu = g1 * sig**3.0
    p12 = _hermnorm(13)
    for k in range(13):
        p12[k] /= sig**k

    # Add all of the terms to polynomial
    totp = (p12[0] - g1/6.0*p12[3] +
            g2/24.0*p12[4] + g1**2/72.0 * p12[6] -
            g3/120.0*p12[5] - g1*g2/144.0*p12[7] - g1**3.0/1296.0*p12[9] +
            g4/720*p12[6] + (g2**2/1152.0 + g1*g3/720)*p12[8] +
            g1**2 * g2/1728.0*p12[10] + g1**4.0 / 31104.0*p12[12])
    # Final normalization
    totp = totp / sqrt(2*pi) / sig

    def thefunc(x):
        xn = (x - mu) / sig
        return totp(xn) * exp(-xn**2 / 2.)

    return thefunc


def _circfuncs_common(samples, high, low):
    samples = np.asarray(samples)
    if samples.size == 0:
        return np.nan, np.nan

    ang = (samples - low)*2*pi / (high - low)
    return samples, ang


def circmean(samples, high=2*pi, low=0, axis=None):
    """
    Compute the circular mean for samples in a range.

    Parameters
    ----------
    samples : array_like
        Input array.
    high : float or int, optional
        High boundary for circular mean range.  Default is ``2*pi``.
    low : float or int, optional
        Low boundary for circular mean range.  Default is 0.
    axis : int, optional
        Axis along which means are computed.  The default is to compute
        the mean of the flattened array.

    Returns
    -------
    circmean : float
        Circular mean.

    """
    samples, ang = _circfuncs_common(samples, high, low)
    res = angle(np.mean(exp(1j * ang), axis=axis))
    mask = res < 0
    if mask.ndim > 0:
        res[mask] += 2*pi
    elif mask:
        res += 2*pi

    return res*(high - low)/2.0/pi + low


def circvar(samples, high=2*pi, low=0, axis=None):
    """
    Compute the circular variance for samples assumed to be in a range

    Parameters
    ----------
    samples : array_like
        Input array.
    low : float or int, optional
        Low boundary for circular variance range.  Default is 0.
    high : float or int, optional
        High boundary for circular variance range.  Default is ``2*pi``.
    axis : int, optional
        Axis along which variances are computed.  The default is to compute
        the variance of the flattened array.

    Returns
    -------
    circvar : float
        Circular variance.

    Notes
    -----
    This uses a definition of circular variance that in the limit of small
    angles returns a number close to the 'linear' variance.

    """
    samples, ang = _circfuncs_common(samples, high, low)
    res = np.mean(exp(1j * ang), axis=axis)
    R = abs(res)
    return ((high - low)/2.0/pi)**2 * 2 * log(1/R)


def circstd(samples, high=2*pi, low=0, axis=None):
    """
    Compute the circular standard deviation for samples assumed to be in the
    range [low to high].

    Parameters
    ----------
    samples : array_like
        Input array.
    low : float or int, optional
        Low boundary for circular standard deviation range.  Default is 0.
    high : float or int, optional
        High boundary for circular standard deviation range.
        Default is ``2*pi``.
    axis : int, optional
        Axis along which standard deviations are computed.  The default is
        to compute the standard deviation of the flattened array.

    Returns
    -------
    circstd : float
        Circular standard deviation.

    Notes
    -----
    This uses a definition of circular standard deviation that in the limit of
    small angles returns a number close to the 'linear' standard deviation.

    """
    samples, ang = _circfuncs_common(samples, high, low)
    res = np.mean(exp(1j * ang), axis=axis)
    R = abs(res)
    return ((high - low)/2.0/pi) * sqrt(-2*log(R))


# Tests to include (from R) -- some of these already in stats.
########
# X Ansari-Bradley
# X Bartlett (and Levene)
# X Binomial
# Y Pearson's Chi-squared (stats.chisquare)
# Y Association Between Paired samples (stats.pearsonr, stats.spearmanr)
#                       stats.kendalltau) -- these need work though
# Fisher's exact test
# X Fligner-Killeen Test
# Y Friedman Rank Sum (stats.friedmanchisquare?)
# Y Kruskal-Wallis
# Y Kolmogorov-Smirnov
# Cochran-Mantel-Haenszel Chi-Squared for Count
# McNemar's Chi-squared for Count
# X Mood Two-Sample
# X Test For Equal Means in One-Way Layout (see stats.ttest also)
# Pairwise Comparisons of proportions
# Pairwise t tests
# Tabulate p values for pairwise comparisons
# Pairwise Wilcoxon rank sum tests
# Power calculations two sample test of prop.
# Power calculations for one and two sample t tests
# Equal or Given Proportions
# Trend in Proportions
# Quade Test
# Y Student's T Test
# Y F Test to compare two variances
# XY Wilcoxon Rank Sum and Signed Rank Tests
