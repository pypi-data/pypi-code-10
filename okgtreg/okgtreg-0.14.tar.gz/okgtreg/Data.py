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
        Given a group structure, either a full partition or a structure consisting of
        a subset of the available covariates, return the corresponding data set and
        the group structure after normalizing the covariate indices.

        The purpose of index normalization is to make the grouped data set look as if
        it is a standalone data set for the subsequent operations. To implement the
        normalization, the smallest covaraite index in the given group is forced to
        be 1 and all the other indices are adjusted accordingly, so that the relative
        differences are not changed. For example:

            ([3, 5], [4], [7, 8])] -> ([1, 3], [2], [5, 6])

        :type group: Group
        :param group: a group structure, either a full partition or a structure consisting
                      of a subset of the available covariates.

        :rtype: tuple(Data, Group)
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
            rawOrders = [np.arange(l) for l in lens]
            return tuple(list(rawOrders[i] + offsets[i]) for i in xrange(len(partition)))

        normalizedPartition = normalizeCovariateIndicesForPartition(group.partition)
        normalizedGroup = Group(*normalizedPartition)
        return subData, normalizedGroup


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

        :rtype: 1d or 2d ndarray
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