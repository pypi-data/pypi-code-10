# This file is part of maggit.
#
# Copyright 2015 Matthieu Gautier <dev@mgautier.fr>
#
# Pit is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# Additional permission under the GNU Affero GPL version 3 section 7:
#
# If you modify this Program, or any covered work, by linking or
# combining it with other code, such other code is not for that reason
# alone subject to any of the requirements of the GNU Affero GPL
# version 3.
#
# You should have received a copy of the GNU Affero General Public License
# along with maggit.  If not, see http://www.gnu.org/licenses
#
# In summary:
# - You can use this program for no cost.
# - You can use this program for both personal and commercial reasons.
# - You do not have to share your own program's code which uses this program.
# - You have to share modifications (e.g bug-fixes, improvements) you've made to this program.

"""
This module contains all the low level classs to handle a git repository.

Class defined in this module use io functions and provide a more consistant API
to access content of the git repository.

Most users will not use those object directly but better use the high level API
provided by the maggit package itself.
"""

from .db import Gitdb
from .repo import Repo
