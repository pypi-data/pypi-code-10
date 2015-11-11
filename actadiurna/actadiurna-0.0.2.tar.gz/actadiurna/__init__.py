#!/usr/bin/env python2.7
#
# Copyright (C) 2015 Joe Block <jpb@unixorn.net.
#
# This program is released under the Apache 2.0 license. See LICENSE

"""
Acta Diurna is a tool to generate an motd file from a directory full of text
files and executables.

Any files it finds in the directory that are not executables will be added to
the motd file verbatim, and any files that are executable will be run and their
output added to the motd file. Files are processed in alphanumeric order.

It defaults to writing to /etc/motd and reading the update fragments
from /etc/update-motd.d
"""

import os
import subprocess


def isExecutable(pathname):
  """Determine if a path is an executable file

  :param str pathname: Path to examine
  :returns: Whether a path is an executable file
  :rtype: boolean
  """
  if os.path.isfile(pathname) and os.access(pathname, os.X_OK):
    return True
  return False


def generateMOTD(output="/etc/motd", updateDirectory="/etc/update-motd.d"):
  """Generate a MOTD file
  :param str output: - file to write the motd to
  :param str updateDirectory: - directory to search for fragment generators
  """
  motd = walkTree(updateDirectory)
  with open(output, "w") as motdFile:
    motdFile.write(motd)


def walkTree(updateDirectory="/etc/update-motd.d"):
  """Walk a directory tree and collect motd output.

  Executable files will be executed, and their output appended to the
  collected data; Regular files will have their contents appended, and
  subdirectories will be walked in turn. Files and subdirectories will be
  processed in alphanumeric order.

  :param str updateDirectory: - directory to search for fragment generators.
  """
  motdData = ""

  fragmentList = os.listdir(updateDirectory)
  fragmentList.sort()
  for cmd in fragmentList:
    commandPath = "%s/%s" % (updateDirectory, cmd)
    if os.path.isfile(commandPath):
      if isExecutable(commandPath):
        motdData = motdData + subprocess.check_output(commandPath)
      else:
        with open(commandPath, 'r') as rawFile:
          motdData = motdData + rawFile.read()
    if os.path.isdir(commandPath):
      motdData = motdData + walkTree(commandPath)
  return motdData
