import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.kernel_approximation import Nystroem


"""
Kernel class object contains a kernel function (callable) and related information.
It also contains some useful methods such as evaluating a gram matrix given data.
"""

class Kernel(object):
    def __init__(self, name, sigma=None, intercept=None, slope=None, degree=None):
        self.name = name
        if name in ('gaussian', 'laplace', 'exponential'):
            if sigma is None:
                raise ValueError("** Parameter 'sigma' is not provided for %s kernel. **" % name)
            else:
                self.sigma = sigma
                if name == 'gaussian':
                    def gaussianKernelFn(x, y):
                        return self.gaussianKernel(x, y, sigma)
                    self.fn = gaussianKernelFn
                elif name == 'laplace':
                    def laplaceKernelFn(x, y):
                        return self.laplaceKernel(x, y, sigma)
                    self.fn = laplaceKernelFn
                elif name == 'exponential':
                    def exponentialKernelFn(x, y):
                        return self.exponentialKernel(x, y, sigma)
                    self.fn = exponentialKernelFn
        elif name == 'polynomial':
            if any(val is None for val in [intercept, slope, degree]):
                raise ValueError("** Parameters 'intercept', 'slope', and 'degree' are not all provided"
                                 "for %s kernel. **" % name)
            else:
                self.intercept = intercept
                self.slope = slope
                self.degree = degree
                def polynomialKernelFn(x, y):
                    return self.polynomialKernel(x, y, intercept, slope, degree)
                self.fn = polynomialKernelFn
        elif name == 'sigmoid':
            if any(val is None for val in [intercept, slope]):
                raise ValueError("** Parameters 'intercept' and 'slope' are not both provided"
                                 "for %s kernel. **" % name)
            else:
                self.intercept = intercept
                self.slope = slope
                def sigmoidKernelFn(x, y):
                    return self.sigmoidKernel(x, y, intercept, slope)
                self.fn = sigmoidKernelFn
        else:
            raise NotImplementedError("** %s kernel is not yet implemented. **" % name)

    def gram(self, x, centered=True):
        # x must be a 2d array
        if x.ndim != 2:
            raise ValueError("** 'x' must be a 2-d array. **")

        n = len(x)
        G = pairwise_distances(x, metric=self.fn)
        # print G
        if centered:
            I = np.identity(n)
            Ones = np.ones((n, n))
            G = (I - Ones / n).dot(G).dot(I - Ones / n) # centered Gram matrix
            return (G + G.T)/2 # numerical issue cause asymmetry
        else:
            return G

    def gram_Nystroem(self, x, nComponents):
        """
        Nystroem approximation of the kernel matrix given data. No centering.

        :type x: 2d array, with size n * p
        :param x: data matrix for the covariates belonging to the same group, associated
                  with the given matrix.

        :type nComponents: int
        :param nComponents: number of rank to retain

        :return: approximated kernel matrix with reduced rank, with size n * nComponents
        """
        nystroem = Nystroem(self.fn, n_components=nComponents)
        return nystroem.fit_transform(x)


    @staticmethod
    def gaussianKernel(x, y, sigma):
            # sigma is a numercial number, x and y are col vectors of same length
            norm2 = np.power(x - y, 2).sum()
            return np.exp(- sigma * norm2)

    @staticmethod
    def laplaceKernel(x, y, sigma):
        absSum = np.abs(x - y).sum()
        return np.exp(-sigma * absSum)

    @staticmethod
    def exponentialKernel(x, y, sigma):
        """
        Exponential kernel function: exp(-sigma * ||x - y||)
        Ref: http://crsouza.org/2010/03/kernel-functions-for-machine-learning-applications/
        """
        # norm = np.sqrt(np.power(x - y, 2).sum())
        norm = np.linalg.norm(x - y)
        return np.exp(-sigma * norm)

    @staticmethod
    def polynomialKernel(x, y, intercept, slope, degree):
        """
        Ref: http://scikit-learn.org/stable/modules/svm.html
        """
        if hasattr(x, "__len__") and hasattr(y, "__len__"):
            # Check if x, y are arrarys, because a scalar cannot use `.sum()`.
            # For example, `(2*3).sum()` causes an error.
            innerprod = (x * y).sum()
        else:
            innerprod = x * y
        return (slope * innerprod + intercept) ** degree

    @staticmethod
    def sigmoidKernel(x, y, intercept, slope):
        """
        Sigmoid kernel function: tanh(a * x * y + r)
        Ref: http://scikit-learn.org/stable/modules/svm.html
        """
        if hasattr(x, "__len__") and hasattr(y, "__len__"):
            innerprod = (x * y).sum()
        else:
            innerprod = x * y
        return np.tanh(slope * innerprod + intercept)