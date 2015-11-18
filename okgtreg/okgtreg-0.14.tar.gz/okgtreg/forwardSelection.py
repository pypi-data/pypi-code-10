# import numpy as np

from .okgtreg import *
from .Parameters import *


"""
Determining group structure by forward selection.
"""

# kernel = Kernel('gaussian', sigma=0.5)


def forwardSelection(data, kernel, useLowRankApproximation=True, rank=10):
    """
    Forward selection procedure for determining group structure for OKGT
    assuming:
     1) all covariates are used
     2) same kernel function (including parameters) is used

    For more details of the algorithm, please refer to my notes.

    :type data: Data
    :param data: data whose structure to be determined

    :type kernel: Kernel
    :param kernel:  kernel function

    :type useLowRankApproximation: boolean
    :param useLowRankApproximation: flag for low rank approximation of kernel matrices.
                                    If True, each kernel matrices are approximated by its
                                    low rank counterpart. Currently, only Nystroem method
                                    is implemented.

    :type rank: int
    :type rank: number of ranks for the low rank approximation.

    :rtype: Group
    :return: selected group structure
    """
    ykernel = kernel

    covariatesPool = list(np.arange(data.p) + 1)
    oldGroup = Group()
    bestR2 = 0.
    # bestOKGT = None
    bestCovariateIndex = None
    # bestGroupIndex = None

    while len(covariatesPool):
        print "** Available covariates: ", covariatesPool
        # add a new group no matter what
        print "** Add as new group: **"
        for covariateInd in covariatesPool:
            print("\t try covariate %d ..." % covariateInd)
            currentGroup = oldGroup.addNewCovariateAsGroup(covariateInd)
            print("\t\t current group structure: %s " % (currentGroup.partition,))
            # The following OKGT needs a subset of data and the grouped covariate
            # indices being normalized, so that the training is done as if we are
            # using a complete data.
            dataForOKGT, groupForOKGT = data.getGroupedData(currentGroup)
            # print groupForOKGT.partition
            # TODO: Currently, using same kernel for all groups.
            # todo: Is it possible to adapt kernels to different group structure?
            xkernels = [kernel] * groupForOKGT.size
            parametersForOKGT = Parameters(groupForOKGT, ykernel, xkernels)
            currentOKGT = OKGTReg(dataForOKGT, parametersForOKGT)
            # Train OKGT
            if useLowRankApproximation:
                res = currentOKGT.train_Nystroem(rank)
            else:
                res = currentOKGT.train_Vanilla()

            currentR2 = res['r2']
            # Check if there is improvement
            if currentR2 > bestR2:
                print("\t\t current R2 =\t %.10f \t *" % currentR2)
                bestR2 = currentR2
                # bestOKGT = currentOKGT
                bestCovariateIndex = covariateInd
                newGroup = currentGroup
            else:
                print("\t\t current R2 =\t %.10f" % currentR2)
            print("\t\t best R2 =\t\t %.10f" % bestR2)
        print("** updated group structure is: %s \n" % (newGroup.partition, ))
        # if group structure is not empty, a new covariate can be added to an existing group
        # print oldGroup.size
        if oldGroup.size is not 0:
            print "** Add to an existing group: **"
            # can add new covariate to existing group
            for covariateInd in covariatesPool:  # pick a covariate
                print("\t try adding covariate %d " % covariateInd)
                for groupInd in np.arange(oldGroup.size)+1:  # pick an existing group
                    # print oldGroup.partition
                    print("\t in group %d ..." % groupInd)
                    currentGroup = oldGroup.addNewCovariateToGroup(covariateInd, groupInd)
                    print("\t\t current group structure: %s " % (currentGroup.partition,))
                    # print currentGroup.partition
                    dataForOKGT, groupForOKGT = data.getGroupedData(currentGroup)
                    # print groupForOKGT.partition
                    xkernels = [kernel] * groupForOKGT.size
                    parametersForOKGT = Parameters(groupForOKGT, ykernel, xkernels)
                    currentOKGT = OKGTReg(dataForOKGT, parametersForOKGT)
                    # Train OKGT
                    if useLowRankApproximation:
                        res = currentOKGT.train_Nystroem(rank)
                    else:
                        res = currentOKGT.train_Vanilla()

                    currentR2 = res['r2']
                    # Check if there is improvement
                    if currentR2 > bestR2:
                        print("\t\t current R2 =\t %.10f \t *" % currentR2)
                        bestR2 = currentR2
                        # bestOKGT = currentOKGT
                        bestCovariateIndex = covariateInd
                        # bestGroupIndex = groupInd
                        newGroup = currentGroup
                    else:
                        print("\t\t current R2 =\t %.10f" % currentR2)
                    print("\t\t best R2 =\t\t %.10f" % bestR2)
        # Add early termination if no further improvement
        # TODO: It is possible that there is no further improvement by adding new
        # todo: covariates, but there are still covaraites in the pool. Currently,
        # todo: I use early termination.
        if newGroup == oldGroup:
            print("** Early termination: %s are still avaliable, "
                  "but no further improvement. ** \n" % covariatesPool)
            break
        else:
            print("** updated group structure is: %s \n" % (newGroup.partition, ))
            covariatesPool.remove(bestCovariateIndex)  # TODO: update in-place, good?
            oldGroup = newGroup

    print ("** SELECTED GROUP STRUCTURE: %s ** \n" % (oldGroup.partition, ))
    # return oldGroup
    return dict(group=oldGroup, r2=bestR2)


