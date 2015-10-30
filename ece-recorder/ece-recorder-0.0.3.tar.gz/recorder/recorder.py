#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

from . import system

def ffmpeg(video, audio, general, output):
    return system.sh("ffmpeg {video_options} {audio_options} {general_options} {output}"
            .format(video_options = video_options,
                    audio_options = audio_options,
                    general_options = general_options,
                    output = output))

def record(acodec, vcodec, threads, output, device_name = "VGA2USB", preset = "ultrafast"):
    video_options = "-f v4l2 -i {device} -vcodec {vcodec}".format(
            device_format = device_fmt,
            device = system.get_video_device(device_name),
            vcodec = vcodec)

    audio_options = "-acodec {acodec}".format(
            acodec = acodec)

    general_options = "-preset {preset} -threads {threads}".format(
            preset = preset,
            threads = threads)

    ffmpeg(video_options, audio_options, general_options, output)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
