#!/usr/bin/env python
# coding=utf-8

"""
This file contains command line constants and functions.
"""

from __future__ import absolute_import
import os
import sys

from demodocus.utilities import print_error

__author__ = "Alberto Pettarin"
__copyright__ = "Copyright 2015, Alberto Pettarin (www.albertopettarin.it)"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "alberto@albertopettarin.it"
__status__ = "Production"


#RES_AUDIO_FILE = os.path.join(os.path.split(os.path.abspath(__file__))[0], "res/sample.mp3")
#RES_JSON_FILE = os.path.join(os.path.split(os.path.abspath(__file__))[0], "res/sample.json")
#RES_SSV_FILE = os.path.join(os.path.split(os.path.abspath(__file__))[0], "res/sample.ssv")
#RES_SSVH_FILE = os.path.join(os.path.split(os.path.abspath(__file__))[0], "res/sample.ssvh")
RES_AUDIO_FILE = "audio.mp3"
RES_JSON_FILE = "syncmap.json"
RES_SSV_FILE = "syncmap.ssv"
RES_SSVH_FILE = "syncmap.ssvh"

COMMAND_LINE_PARAMETERS = [
    {
        "short": "-a",
        "long": "--audio",
        "help": "path to the audio file",
        "action": "store"
    },
    {
        "short": "-c",
        "long": "--continuous",
        "help": "keep going (default: False)",
        "action": "store_true"
    },
    {
        "short": "-d",
        "long": "--duration",
        "help": "play audio for max DURATION seconds (default: 2)",
        "action": "store"
    },
    {
        "short": "-i",
        "long": "--increment",
        "help": "play audio every INCREMENT fragments (default: 1)",
        "action": "store"
    },
    {
        "short": "-s",
        "long": "--syncmap",
        "help": "path to the sync map file",
        "action": "store"
    },
    {
        "short": "-v",
        "long": "--version",
        "help": "print version and exit",
        "action": "store_true"
    },
    {
        "short": "-w",
        "long": "--wait",
        "help": "wait WAIT seconds before playing the next fragment (default: 0)",
        "action": "store"
    },
]

REQUIRED_PARAMETERS = [
    "audio",
    "syncmap"
]

EXAMPLES = [
    #{
    #    "options": "-h",
    #    "description": "Print this message and exit"
    #},
    #{
    #    "options": "-v",
    #    "description": "Print the version and exit"
    #},
    {
        "options": "-a %s -s %s" % (RES_AUDIO_FILE, RES_JSON_FILE),
        "description": "Check %s against %s with default parameters (2 seconds, all fragments)" % (RES_AUDIO_FILE, RES_JSON_FILE)
    },
    {
        "options": "-a %s -s %s" % (RES_AUDIO_FILE, RES_SSV_FILE),
        "description": "As above, but the sync map file has SSV format"
    },
    {
        "options": "-a %s -s %s -d 1" % (RES_AUDIO_FILE, RES_JSON_FILE),
        "description": "Play each fragment for max 1 second"
    },
    {
        "options": "-a %s -s %s -d 3 -i 5" % (RES_AUDIO_FILE, RES_JSON_FILE),
        "description": "Play every 5 fragments, for max 3 seconds each"
    },
    {
        "options": "-a %s -s %s -d 3 -i 5 -w 0.5" % (RES_AUDIO_FILE, RES_JSON_FILE),
        "description": "Pause for 0.5 seconds before playing next fragment"
    },
    {
        "options": "-a %s -s %s -c -i 5 -d 1.5 -w 0.5" % (RES_AUDIO_FILE, RES_JSON_FILE),
        "description": "Play every 5 fragments, 1.5 seconds each, continuously, pausing for 0.5 seconds"
    }
]

USAGE = u"""
  $ demodocus -h
  $ demodocus -a AUDIO -s SYNCMAP [OPTIONS]
"""

DESCRIPTION = u"""description:
  Run an interactive CLI tool to verify that SYNCMAP has a good alignment against AUDIO.
  The sync map file can be in JSON or SSV/SSVH format (auto-detected)."""

EPILOG = u"examples:\n"
for example in EXAMPLES:
    EPILOG += u"\n"
    EPILOG += u"  $ demodocus %s\n" % (example["options"])
    EPILOG += u"    %s\n" % (example["description"])
EPILOG += u"  \n"

def check_arguments(args):
    """
    Check that we have all the required command line arguments,
    and that the input/output format values are supported.
    """
    for required in REQUIRED_PARAMETERS:
        if required not in args:
            print_error("Argument '%s' is required" % required)
            sys.exit(2)

def set_default_values(args):
    def set_default_value(key, value):
        if not args.__contains__(key):
            args.__dict__[key] = value
    set_default_value("continuous", False)
    set_default_value("duration", 2)
    set_default_value("increment", 1)
    set_default_value("wait", 0)



