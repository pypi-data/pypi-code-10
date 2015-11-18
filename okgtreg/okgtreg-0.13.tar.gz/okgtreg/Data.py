# from okgtreg.Group import *
from .Group import *

"""
Classes for data
"""

class Data(object):
    """
    Encapsulating data including: response, covariate matrix, sample size,
    covariate dimension. Also included is a method to create a grouped data.
    """
    def __init__(self, y, X):
        self.y = y
        self.X = X
        self.n = len(y)  # sample size
        self.p = X.shape[1]  # covariate dimension

    def getGroupedData(self, group):
        """

        :type group: Group
        :param group: a group structure

        :type return: tuple(Data, Group)
        :return: grouped data, i.e. Data(y, subset of X), and
                 a group structure with covariate indices being
                 normalized.
        """
        def flattenPartition(partition):
            return [i for g in partition for i in g]

        covariateInds = flattenPartition(group.partition)
        subX = self.X[:, np.array(covariateInds)-1]
        y = self.y
        subData = Data(y, subX)

        def normalizeCovariateIndicesForPartition(partition):
            # partition is a tuple of lists
            lens = [len(g) for g in partition]
            offsets = np.array(lens).cumsum() - lens + 1
            rawOrders = [np.arange(l)  for l in lens]
            return tuple(list(rawOrders[i] + offsets[i]) for i in xrange(len(partition)))

        normalizedPartition = normalizeCovariateIndicesForPartition(group.partition)
        normalizedGroup = Group(*normalizedPartition)
        return subData, normalizedGroup


    # def groupData(self, group):
    #     """
    #     Creating grouped data by giving group structure information for the covariates.
    #
    #     :type group: Group
    #     :param group: group structure of covariates
    #
    #     :type return: GroupedData
    #     :return: data with group structure information
    #     """
    #     if group.p != self.p:
    #         raise ValueError("** Group structure is not conformable to X. **")
    #
    #     return GroupedData(self.y, self.X, group)


# class GroupedData(Data):
#     """
#     Encapsulating data with group structure information.
#     """
#     def __init__(self, y, X, group):
#         """
#
#         :type y: 1d ndarry
#         :param y: response vector
#
#         :type X: 1d or 2d ndarry
#         :param X: covariate matrix
#
#         :type group: Group
#         :param group: group structure of covariates
#
#         :return: nothing
#         """
#         if group.p != X.shape[1]:
#             raise ValueError("** Group structure is not conformable to X. **")
#
#         Data.__init__(self, y, X)
#         self.group = group
#         self.partition = group.partition
#         self.groupSize = group.size
#
#     def getGroup(self, groupNumber = None):
#         """
#         Return the data sub-matrix of the covariate matrix, corresponding to
#         the given group number. The group number starts from 1.
#
#         :type groupNumber: None or int
#         :param groupNumber: the group number whose covariate sub-matrix is returned. If None, by default,
#                             the whole covariate matrix is returned.
#
#         :type return: 1d or 2d ndarray
#         :return: covariate sub-matrix
#         """
#         if groupNumber is None:
#             return self.X
#         else:
#             if groupNumber <= 0 or groupNumber > self.groupSize:
#                 raise ValueError("** 'groupNumber' is out of bound. **")
#
#             cols = np.array(self.partition[groupNumber - 1])  # group number start from 1
#             return self.X[:, cols - 1]
#
#     def equipKernels(self, ykernel, xkernels):
#         """
#         Associate each group in a group structure with a kernel.
#
#         :type ykernel: Kernel
#         :param ykernel: kernel for response
#
#         :param xkernels: list of Kernel objects
#         :param xkernels: a list of kernels for covariates, one for each group
#
#         :type return: GroupedDataWithKernels
#         :return: data with group structure information and each group is associated with a kernel
#         """
#         if len(xkernels) != self.groupSize:
#             raise ValueError("** The number of kernels is not conformable to the group size. "
#                              "There are %d kernels and %d groups. **" % (len(xkernels), self.groupSize))
#
#         return GroupedDataWithKernels(self.y, self.X, self.group, ykernel, xkernels)


# class GroupedDataWithKernels(GroupedData):
#     """
#     Encapsulating data with group and kernel information.
#     """
#     def __init__(self, y, X, group, ykernel, xkernels):
#         """
#
#         :type y: 1d ndarray
#         :param y: response vector
#
#         :type X: 1d or 2d ndarray
#         :param X: covariate matrix
#
#         :type group: Group
#         :param group: group structure
#
#         :type ykernel: Kernel
#         :param ykernel: kernel for response
#
#         :type xkernels: list of Kernel objects
#         :param xkernels: one kernel for each group of covariates
#
#         :return: nothing
#         """
#         if len(xkernels) != group.size:
#             raise ValueError("** The number of x kernels is not conformable to the group size."
#                              "There are %d kernels and %d groups. **" % (len(xkernels), group.size))
#
#         GroupedData.__init__(self, y, X, group)
#         self.ykernel = ykernel
#         self.xkernels = xkernels
#
#     # used to construct covariance and cross-covariance operators
#     # private methods
#     def _stackGramsForX(self):
#         grams = [kernel.gram(self.getGroup(i+1)) for (i, kernel) in enumerate(self.xkernels)]
#         return np.vstack(grams)
#
#     def covarianceOperator(self):
#         vstackedGrams = self._stackGramsForX()
#         cov = vstackedGrams.dot(vstackedGrams.T) / self.n
#         return cov
#
#     def crossCovarianceOperator(self):
#         # return R_yx: H_x -> H_y
#         yGram = self.ykernel.gram(self.y[:, np.newaxis])  # need kernel for y
#         xStackedGrams = self._stackGramsForX()
#         crossCov = yGram.dot(xStackedGrams.T) / self.n
#         return crossCov


class ParameterizedData(object):
    def __init__(self, data, parameters):
        if data.p != parameters.p:
            raise ValueError("** Covariates dimensions for data and parameters are not conformable."
                             "Data has %d covariates, while parameters have %d covariates." % (data.p, parameters.p))

        self.p = data.p
        self.n = data.n
        self.y = data.y
        self.X = data.X
        self.partition = parameters.partition
        self.groupSize = parameters.groupSize
        self.ykernel = parameters.ykernel
        self.xkernels = parameters.xkernels

    def getXFromGroup(self, groupNumber = None):
        """
        Return the data sub-matrix of the covariate matrix, corresponding to
        the given group number. The group number starts from 1.

        :type groupNumber: None or int
        :param groupNumber: the group number whose covariate sub-matrix is returned. If None, by default,
                            the whole covariate matrix is returned.

        :type return: 1d or 2d ndarray
        :return: covariate sub-matrix
        """
        if groupNumber is None:
            return self.X
        else:
            if groupNumber <= 0 or groupNumber > self.groupSize:
                raise ValueError("** 'groupNumber' is out of bound. **")

            cols = np.array(self.partition[groupNumber - 1])  # group number start from 1
            return self.X[:, cols - 1]

    def _stackGramsForX(self):
        grams = [kernel.gram(self.getXFromGroup(i+1)) for (i, kernel) in enumerate(self.xkernels)]
        return np.vstack(grams)

    def covarianceOperatorForX(self, returnAll=False):
        vstackedGrams = self._stackGramsForX()
        cov = vstackedGrams.dot(vstackedGrams.T) / self.n
        if returnAll:
            return cov, vstackedGrams
        else:
            return cov

    def covarianceOperatorForY(self, returnAll=False):
        yGram = self.ykernel.gram(self.y[:, np.newaxis])
        cov = yGram.dot(yGram.T) / self.n
        if returnAll:
            return cov, yGram
        else:
            return cov

    def crossCovarianceOperator(self):
        # return R_yx: H_x -> H_y
        yGram = self.ykernel.gram(self.y[:, np.newaxis])  # need kernel for y
        xStackedGrams = self._stackGramsForX()
        crossCov = yGram.dot(xStackedGrams.T) / self.n
        return crossCov