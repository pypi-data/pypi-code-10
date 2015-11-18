import numpy as np

from okgtreg.Group import *
from okgtreg.okgtreg import *
from okgtreg.DataSimulator import *


"""
Determining group structure by backward selection.
We start from a fully non-parametric model, i.e.

    g(y) = f(x_1, x_2, ..., x_p)

and record its r2.

Then for each one in the pool of available variables,
we try the following operations:

1. Create a new group where the selected variable is
   the only memeber. Then, okgt is fitted using the new
   group structure.

2. If there are other groups than the pool group we
   started from, the selected variable joins each
   of the other groups to form a new group structure.
   Then, okgt is fitted using the new group structure.

During each operation, the new r2 is compared with the
old r2 to check if there is improvement. If r2 increases,
r2 is updated.

The above procedure continues until one of the following
conditions is met:

1. r2 stops increasing
2. there is only one variable remaining in the pool

The second condition is set to avoid redundancy. For example,
if there are two variable in total (x1, x2). The possible
group structures are either (x1, x2) or [(x1), (x2)]. That is,
once a variable is separated from the other, the procedure
is done. There is no need to test for the last variable in the
pool.
"""

# ------------------------
# Start forward selection
# ------------------------
def backwardSelection(data, kernel, useLowRankApproximation=True, rank=10):
    # useLowRankApproximation = True
    # rank = 10

    ykernel = kernel

    covariatesPool = list(np.arange(data.p) + 1)
    oldGroup = Group(covariatesPool)
    p = oldGroup.p
    bestR2 = 0.
    bestCovariateIndex = None

    counter = 0

    while len(covariatesPool) > 1:
        counter += 1
        print("** === Step %d === **" % counter)
        # Create a new group
        print("** Create a new group: **")
        for covariateInd in covariatesPool:
            print("\t Create a new group for covariate %d ..." % covariateInd)
            _currentGroup = oldGroup.removeOneCovariate(covariateInd)
            currentGroup = _currentGroup.addNewCovariateAsGroup(covariateInd)
            print("\t\t current group structure: %s " % (currentGroup.partition,))
            # Contrary to forward selection, the data matrix doesn't
            # change.
            xkernels = [kernel] * currentGroup.size
            parameters = Parameters(currentGroup, ykernel, xkernels)
            currentOKGT = OKGTReg(data, parameters)
            # Train OKGT
            if useLowRankApproximation:
                res = currentOKGT.train_Nystroem(rank)
            else:
                res = currentOKGT.train_Vanilla()

            currentR2 = res['r2']
            if currentR2 > bestR2:
                print("\t\t current R2 =\t %.10f \t *" % currentR2)
                bestR2 = currentR2
                newGroup = currentGroup
                bestCovariateIndex = covariateInd
            else:
                print("\t\t current R2 =\t %.10f" % currentR2)
            print("\t\t best R2 =\t\t %.10f \n" % bestR2)

        # print("** Updated group structure is: %s \n" % (newGroup.partition, ))
        # print '\n'
        # If there are already new groups, a chosen variable can join one of the
        # new groups instead of creating a new group.
        print "** Add to an existing group: **"
        if oldGroup.size > 1:
            for covariateInd in covariatesPool:
                print("\t try adding covariate %d " % covariateInd)
                # Remove `covariateInd`-th covariate from the pool,
                # which will be added into one of the other groups.
                updatedCovariatesPool = copy.deepcopy(covariatesPool)
                updatedCovariatesPool.remove(covariateInd)
                # Get the group number of the chosen `covariateInd`
                covariateMember = oldGroup.getMembership(covariateInd)
                # Take all other groups as a Group object
                otherGroupInds = list(np.arange(oldGroup.size)+1)
                otherGroupInds.remove(covariateMember)

                # print type(otherGroupInds), ": ", otherGroupInds

                otherGroup = oldGroup.getPartitions(otherGroupInds, True)
                # Try adding the chosen `covariateInd` to each of the other groups
                for groupInd in np.arange(otherGroup.size) + 1:
                    print("\t   in other group %d ..." % groupInd)
                    updatedOtherGroup = otherGroup.addNewCovariateToGroup(covariateInd, groupInd)
                    currentGroup = updatedOtherGroup + updatedCovariatesPool
                    print("\t\t current group structure: %s " % (currentGroup.partition,))
                    xkernels = [kernel] * currentGroup.size
                    parameters = Parameters(currentGroup, ykernel, xkernels)
                    currentOKGT = OKGTReg(data, parameters)
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
                        newGroup = currentGroup
                        bestCovariateIndex = covariateInd
                    else:
                        print("\t\t current R2 =\t %.10f" % currentR2)
                    print("\t\t best R2 =\t\t %.10f \n" % bestR2)
        else:
            print("\t ** No other groups than the pool. Pass ... ** \n")

        print("** Step %d updated group structure is: %s \n" % (counter, newGroup.partition))

        # print "covariate pool: ", covariatesPool
        # print "best covariate index so far: ", bestCovariateIndex

        if bestCovariateIndex in covariatesPool:
            covariatesPool.remove(bestCovariateIndex)
            oldGroup = newGroup
            if counter == p-1:
                print("** Finish with complete iterations. ** \n")
        else:
            print("** Finish with early termination at step %d due to no further improvement of R2. ** \n" % counter)
            break

    print ("** SELECTED GROUP STRUCTURE: %s with R2 = %f ** \n" % (oldGroup.partition, bestR2))
    return oldGroup


if __name__ == "__main__":
    # Simulate data
    np.random.seed(25)
    # y, x = DataSimulator.SimData_Wang04(500)
    y, x = DataSimulator.SimData_Wang04WithInteraction(500)
    data = Data(y, x)

    # Same kernel for all groups
    kernel = Kernel('gaussian', sigma=0.5)

    # Call backward selection
    selectedGroup = backwardSelection(data, kernel, True, 10)