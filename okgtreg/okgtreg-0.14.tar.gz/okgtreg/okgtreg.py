import scipy as sp
import scipy.linalg as slin

from .Data import *
from .Kernel import *


"""
X: covariate matrix (high dimensional)
y: response vector (univariate)
groupStructure: partition of variables into groups
"""

####################
# Classes for Data #
####################

# Moved to Data.py

#############################
# Class for Group Structure #
#############################

# Moved to Group.py

################
# Kernel Class #
################

# Moved to Kernel.py

####################
# Parameters class #
####################

# Moved to Parameters.py


#################
# OKGTReg class #
#################
eps=1e-6

class OKGTReg(object):
    def __init__(self, data, parameters):
        """

        :type data: Data
        :param data:

        :type params: Parameters
        :param params:

        :rtype: OKGTReg
        :return:
        """
        # private field, not to accessed directly
        self.parameterizedData = ParameterizedData(data, parameters)

    def getX(self):
        return self.parameterizedData.X

    def getY(self):
        return self.parameterizedData.y

    def getKernels(self, yOrX):
        """

        :param yOrX:

        :type return: Kernel or list of Kernel objects
        :return:
        """
        if yOrX is 'y':
            return self.parameterizedData.ykernel
        else:
            return self.parameterizedData.xkernels

    def getPartition(self):
        return self.parameterizedData.partition

    def getSampleSize(self):
        return self.parameterizedData.n

    def getGroupSize(self):
        return self.parameterizedData.groupSize

    def train_Vanilla(self):
        n = self.getSampleSize()
        l = self.getGroupSize()

        # print "** Start OKGT Training (Vanilla)**"

        Rxx, Gx = self.parameterizedData.covarianceOperatorForX(returnAll=True)
        Ryy, Gy = self.parameterizedData.covarianceOperatorForY(returnAll=True)
        # Ryx = self.parameterizedData.crossCovarianceOperator()
        Ryx = Gy.dot(Gx.T) / n

        D, P = np.linalg.eigh(Ryy + eps * np.identity(n))
        D = D[::-1]
        P = P[:, ::-1]
        D_inv = np.diag(1. / np.sqrt(D))
        Gy_inv = D_inv.dot(P.T) # Ryy^{-1/2}

        Rxx_inv = np.linalg.inv(Rxx + eps * np.identity(n * l))

        #TODO: if Rxx is large, the inverse would be slow.
        VyxVxy = reduce(np.dot, [Gy_inv, Ryx, Rxx_inv, Ryx.T, Gy_inv.T])

        # g: optimal transformation for y
        r2, beta = slin.eigh(VyxVxy, eigvals=(n-1, n-1)) # only need the largest eigen value and vector
        _zeta = D_inv.dot(beta)
        zeta = P.dot(_zeta)
        g_opt = Gy.dot(zeta)

        # f: optimal transformation for x
        # TODO: use matrix multiplication to replace the following loop
        _x_i = Ryx.T.dot(g_opt)
        x_i = Rxx_inv.dot(_x_i)
        f_opt_ls = []
        for i in range(l):
            x_ii = x_i[i*n : (i+1)*n]
            Gx_i = Gx[i*n : (i+1)*n, :]
            f_i_opt = Gx_i.dot(x_ii)
            f_i_norm = np.sqrt(x_ii.T.dot(f_i_opt))
            f_i_opt = f_i_opt / f_i_norm
            f_opt_ls.append(f_i_opt)

        f_opt = np.column_stack(f_opt_ls)

        # print "** Success **"
        return dict(g=g_opt, f=f_opt, r2=float(r2))

    def train_Nystroem(self, nComponents):
        n = self.getSampleSize()
        l = self.getGroupSize()

        # print "** Start OKGT Training (Nystroem) **"

        N0 = np.identity(n) - np.ones((n, n)) / n
        ykernel = self.getKernels('y')
        Gy = ykernel.gram_Nystroem(self.getY()[:, np.newaxis], nComponents)
        Uy, Gy_s, Gy_V = np.linalg.svd(N0.dot(Gy), full_matrices=0)
        lambday = Gy_s**2
        my = len(Gy_s)

        Ux = []
        lambdax = []
        xkernels = self.getKernels('x')  # list of Kernels for X, one for each group
        for i in range(l):
            inds = [ind - 1 for ind in self.getPartition()[i]] # column index for i-th group
            Gi = xkernels[i].gram_Nystroem(self.getX()[:, inds], nComponents)
            Ui, Gi_s, Gi_V = np.linalg.svd(N0.dot(Gi), full_matrices=0)
            Ux.append(Ui)
            lambdai = Gi_s**2
            lambdax.append(lambdai)

        lambdax_row = np.hstack(lambdax)
        Ux_row = np.hstack(Ux)
        Ux_diag = sp.sparse.block_diag(Ux)

        T = reduce(np.dot, [np.diag(lambday / (lambday + eps)), Uy.T, Ux_row, np.diag(lambdax_row)])
        R = np.diag((lambdax_row + eps)**2) + \
                reduce(np.dot, [np.diag(lambdax_row),
                               Ux_row.T.dot(Ux_row) - np.identity(len(lambdax_row)),
                               np.diag(lambdax_row)])
        R_inv = np.linalg.inv(R)  # much faster now
        vv = reduce(np.dot, [T, R_inv, T.T])

        eigval, eigvec = sp.linalg.eigh(vv, eigvals=(my-1, my-1))
        r2 = float(eigval)
        _g_opt = np.diag(lambday).dot(eigvec)
        g_opt = Uy.dot(_g_opt)

        _f_opt = np.diag(np.sqrt(lambday**2 + eps) * lambday).dot(eigvec)
        _f_opt = T.T.dot(_f_opt)
        _f_opt = R_inv.dot(_f_opt)
        _f_opt = np.diag(lambdax_row).dot(_f_opt)
        _f_opt = Ux_diag.dot(_f_opt)
        f_opt =  _f_opt.reshape((n, l), order='F')

        # print "** Success **"
        return dict(g=g_opt, f=f_opt, r2=r2)
