#!/usr/bin/env python

"""Map functions onto image arrays."""


import numpy

from . import image


def map_to_channels(func, img):
    """Map a function onto the channels of an image array."""
    channels = image.get_channels(img)
    first = next(channels)
    z = func(first)
    for channel in channels:
        z = numpy.dstack((z, func(channel)))
    return z


if __name__ == '__main__':
    pass
