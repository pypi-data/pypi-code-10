#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, subprocess, logging

from . import utils

logger = logging.getLogger(__name__)

def sh(cmd):
    logger.debug(cmd)
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).call() == 0

def read_file(path):
    content = None
    with open(path, 'r') as f:
        content = f.read()
    return content.strip()

def video_devices():
    device_root = '/sys/class/video4linux'
    try:
        for device in os.listdir(device_root):
            for root,dirs,files in os.walk(os.path.join(device_root, device)):
                yield (os.path.basename(root), read_file(os.path.join(root, 'name')))
                break
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise Exception("no video4linux devices found in %s!" % device_root)
        else:
            raise

def get_video_device(name):
    device_names = []
    for device, device_name in video_devices():
        if name in device_name:
            return "/dev/%s" % device
        else:
            device_names.append(device_name)

    raise Exception("could not find device %s %s" % (name, device_names))

def ffmpeg(global_opts, video_opts, audio_opts, output_opts, output_path):
    logger.debug(global_opts)
    logger.debug(video_opts)
    logger.debug(audio_opts)
    logger.debug(general_opts)
    logger.debug(output_opts)

    return system.sh(format(
        "ffmpeg {global_options} {video_options} {audio_options} {output_options} {output}",
        global_options = global_opts,
        video_options = video_opts,
        audio_options = audio_opts,
        output_options = output_opts,
        output = output_path))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
