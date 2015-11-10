# coding=utf-8
"""A Python Package for multi-processing/threading ssh connections in order to make ssh operations
across multiple servers more parallel.  The module allows for timeouts for each ssh connection
as well as each command given to an ssh connection to run.  ServerJob objects allow for each server
to have multiple commands that should be run inside of a single job.  The results
from each job will be returned as a list of tuples inside of each ServerJob object in the same order that the
commands are sent in.

The SSH Module can also be used to create and call ssh connections without multiple processes/threads.

SSHreader can also run multi-processed/threaded shell commands on localhost and a serverJobList can contain both
serverJobs running on localhost as well as serverJobs running over ssh.

Threads vs. sub-Processes vs. (sub-Processes and Threads)
---------------------------------------------------------

When using **pcount** and **tcount** in conjunction, tcount will equal the total number of threads each process is
allowed to spawn.  If the total jobs per process is less than tcount then the number of threads per process will equal
the number of jobs assigned to that process.  Thus, to find the total threads used across all processes use:

    (pcount * tcount) = total_threads

When using pcount, sshreader attempts to ensure that jobs are split evenly between the number of requested
sub-processes.

Limitations
-----------

**ServerJob**:

The sshread method currently limits you to processing 1 million ServerJobs at a time [1]_ , per \_\_jobHardLimit__ global.


**cpusoftlimit**:

The cpusoftlimit for a box is defined as:

    (cpu_count - 1)

This means that sshreader will spawn a sub-process for all but one cpu on a given box.

**cpuhardlimit**:

The cpuhardlimit is the maximum number of sub-processes that sshreader will spawn on a given box defined as:

    (cpuhardlimit * \_\_cpuHardLimitFactor__).

This is so that you don't make a box unusable and was arrived at per my own testing.  Currently,
\_\_cpuHardLimitFactor__ is set to 3 [1]_ .

.. [1] These numbers may increase in the future.
"""
# Copyright (C) 2015 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function
from pkg_resources import get_distribution, DistributionNotFound

# TODO - Get this module working in Python 3!
# For backwards compatibility
from ssh import SSH, do_shell_script
from sshreader import ServerJob, sshread, print_results, progress_bar

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
try:
    __version__ = get_distribution('sshreader').version
except DistributionNotFound:
    __version__ = 'UNKNOWN'
__all__ = ['sshreader', 'ssh']
