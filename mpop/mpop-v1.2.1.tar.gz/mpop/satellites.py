#!/usr/bin/python
# Copyright (c) 2015.
#

# Author(s):
#   Martin Raspaud <martin.raspaud@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""Backward compatibility
"""

from mpop.scene import Scene
import warnings
warnings.simplefilter('always', DeprecationWarning)

def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)

class GeostationaryFactory(object):

    """Factory for geostationary satellite scenes.
    """

    @staticmethod
    def create_scene(satname, satnumber, instrument, time_slot, area=None,
                     variant=''):
        """Create a compound satellite scene.
        """
        deprecation("Please, don't use that")

        return GenericFactory.create_scene(satname, satnumber, instrument,
                                           time_slot, None, area, variant)


class PolarFactory(object):

    """Factory for polar satellite scenes.
    """

    deprecation("Please, don't use that")

    @staticmethod
    def create_scene(satname, satnumber, instrument, time_slot, orbit=None,
                     area=None, variant=''):
        """Create a compound satellite scene.
        """

        return GenericFactory.create_scene(satname, satnumber, instrument,
                                           time_slot, orbit, area, variant)


class GenericFactory(object):

    """Factory for generic satellite scenes.
    """

    deprecation("Please, don't use that")

    @staticmethod
    def create_scene(satname, satnumber, instrument, time_slot, orbit,
                     area=None, variant=''):
        """Create a compound satellite scene.
        """

        satellite = (satname, satnumber, variant)
        return Scene(platform_name=variant+satname+satnumber, sensor=instrument,
                     start_time=time_slot, area=area)
        return instrument_scene