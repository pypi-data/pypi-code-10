#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Copyright 2009-2014 Ghent University
#
# This file is part of vsc-base,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/vsc-base
#
# vsc-base is free software: you can redistribute it and/or modify
# it under the terms of the GNU Library General Public License as
# published by the Free Software Foundation, either version 2 of
# the License, or (at your option) any later version.
#
# vsc-base is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with vsc-base. If not, see <http://www.gnu.org/licenses/>.
#
"""
vsc-base base distribution setup.py

@author: Stijn De Weirdt (Ghent University)
@author: Andy Georges (Ghent University)
@author: Kenneth Hoste (Ghent University)
"""


# Inserted shared_setup_dist_only
# Based on shared_setup version 0.9.3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'external_dist_only'))

import shared_setup_dist_only as shared_setup
from shared_setup_dist_only import ag, kh, jt, sdw, URL_GH_HPCUGENT

VSC_INSTALL_REQ_VERSION = '0.9.3'

PACKAGE = {
    'name': 'vsc-base',
    'version': '2.4.12',
    'author': [sdw, jt, ag, kh],
    'maintainer': [sdw, jt, ag, kh],
    'scripts': ['bin/logdaemon.py', 'bin/startlogdaemon.sh', 'bin/bdist_rpm.sh', 'bin/optcomplete.bash'],
    'install_requires': ['vsc-install >= %s' % VSC_INSTALL_REQ_VERSION], # as long as 1.0.0 is not out, vsc-base should still provide vsc.fancylogger
    'setup_requires': ['vsc-install >= %s' % VSC_INSTALL_REQ_VERSION],
    'zip_safe': True,
}

if __name__ == '__main__':
    shared_setup.action_target(PACKAGE, urltemplate=URL_GH_HPCUGENT)
