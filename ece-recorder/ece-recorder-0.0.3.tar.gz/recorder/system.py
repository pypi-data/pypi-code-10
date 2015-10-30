#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os, subprocess

def sh(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).call()

def read_file(path):
    content = None
    with open(path, 'r') as f:
        content = f.read()
    return content.strip()

def video_devices():
    try:
        for device in os.listdir('/sys/class/video4linux'):
            for root,dirs,files in os.walk(os.path.join('/sys/class/video4linux', device)):
                yield (os.path.basename(root), read_file(os.path.join(root, 'name')))
                break
    except FileNotFoundError:
        raise Exception("no v4l devices found!")

def get_video_device(name):
    for device, device_name in video_devices():
        if name in device_name:
            return "/dev/%s" % device

    raise Exception("could not find device %s" % name)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
