
# Note: alpha/beta version should not be delivered to customer
#       only ('alpha', 'beta', 'rc', 'final') used
#       {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
VERSION = (0, 6, 6, 'final', 0)


def get_version():
    """
    :return:
    """
    from tingyun.version import get_version
    return get_version(VERSION)
