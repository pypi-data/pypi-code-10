class Parameters(object):
    """
    Encapsulating the model parameters: group structure and kernels
    """
    def __init__(self, group, ykernel, xkernels):
        """

        :type group: Group
        :param group:
        :type kernels: list of Kernel objects
        :param kernels:
        :return:
        """
        if group.size != len(xkernels):
            raise ValueError("** Each group must be equipped with a kernel. "
                             "There are %d groups, and %d kernels. ** " % (group.size, len(xkernels)))
        else:
            self.p = group.p
            self.partition = group.partition
            self.groupSize = group.size
            self.ykernel = ykernel
            self.xkernels = xkernels

