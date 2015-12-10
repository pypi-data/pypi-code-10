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

from setuptools import setup, find_packages

setup(name='maggit',
      version='0.1',
      description="A python implemetation of git",
      author="Matthieu Gautier",
      author_email="dev@mgautier.fr",
      license = 'AGPLv3+ with "Lesser" clause',
      classifiers=['Operating System :: OS Independent',
                   'Programming Language :: Python :: 3.4',
                   'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                   'Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries :: Python Modules'
                  ],
      packages=find_packages(exclude=['tests']),
      keywords="git",
)

