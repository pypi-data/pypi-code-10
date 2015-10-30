#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

VERSION = "0.0.6"

import os

from . import system

def record(acodec, vcodec, threads, output, device_name = "VGA2USB", preset = "ultrafast"):
    if os.path.splitext(output)[1] == '':
        raise Exception("no format specified for output file: %s" % output)

    video_options = "-f v4l2 -i {device} -vcodec {vcodec}".format(
            device = system.get_video_device(device_name),
            vcodec = vcodec)

    audio_options = "-acodec {acodec}".format(
            acodec = acodec)

    general_options = "-preset {preset} -threads {threads}".format(
            preset = preset,
            threads = threads)

    system.ffmpeg(video_options, audio_options, general_options, output)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
