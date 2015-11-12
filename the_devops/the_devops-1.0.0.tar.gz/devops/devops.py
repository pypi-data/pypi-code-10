#!/usr/bin/python

"""
This DevOps library allows the user to 'totally devops'.

Author:     David Gee
Date:       10th November 2015
Version:    0.1
"""

THE_DEVOPS = "Dude, you totally devopsificated"


class devops(object):
    """
    DevOps object. Doesn't do anything other than the devops magic.

    Methods:    n/a
    Returns:    n/a
    Raises:     n/a

    Usage:
    >>> mydevops = devops()
    >>> print mydevops
    Dude, you totally devopsificated
    """

    def __init__(self):
        """
        Object init. Requires nothing.

        Init:       Object init for DevOps
        Requires:   n/a
        Returns:    n/a
        Raises:     n/a
        """
        pass

    def __str__(self):
        """Method returns THE_DEVOPS var."""
        return THE_DEVOPS
