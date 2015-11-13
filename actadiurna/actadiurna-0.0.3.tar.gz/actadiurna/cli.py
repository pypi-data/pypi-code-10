#!/usr/bin/env python2.7
#
# Copyright (C) 2015 Joe Block. All rights reserved.
#
# This program is released under the Apache 2.0 license. See LICENSE.
"""
Need a driver for setup.py to use in the entry_points array
"""

import argparse

from actadiurna import generateMOTD


def actaMain():
  """Driver script for setup.py to use as an entry point"""

  parser = argparse.ArgumentParser()

  parser.add_argument("--update-directory",
                      dest="updateDirectory",
                      help="Specify directory to load fragment files from",
                      default="/etc/update-motd.d")

  parser.add_argument("--output",
                      help="Specify output file",
                      default="/etc/motd")

  args = parser.parse_args()
  generateMOTD(output=args.output, updateDirectory=args.updateDirectory)


if __name__ == "__main__":
  actaMain()
