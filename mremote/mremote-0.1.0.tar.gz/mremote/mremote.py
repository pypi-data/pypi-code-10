#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Flask based API.
    Requires ircsend to work.
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from scipy.spatial import distance
import subprocess
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
COLORS_FILE = os.path.join(BASE_DIR, 'base_colors.json')
CONF_FILE = os.path.join("/etc/lirc/lircd.conf")


def get_base_colors(COLORS_FILE):
    """
        Extracts base config from a json.
        Color format is [rrr,ggg,bbb] (0..255)
        The buttons configured in CONF_FILE with irrecord must be named
        rrr_ggg_bbb as in the json file
    """
    return json.load(open(COLORS_FILE))


def read_lirc_file():
    """
        Reads a LIRC config file
        and extrats the remotes and buttons =)
    """

    def make_groups(lines, start, end, name):
        """
            Generic grouping.
            Gets a file in the form

            start
            asdfasdf
            asdfasdf
            end
            start
            123123123
            123123123
            end

            and returns groups (asdfasdf, asdfasdf), (123123123, 123123123)
        """
        starts = []
        ends = []

        for n, line in enumerate(lines):
            if "{} {}".format(start, name) in line:
                starts.append(n)
            elif "{} {}".format(end, name) in line:
                ends.append(n)
        return zip(starts, ends)

    def clean(phrase):
        """
            Cleanses spaces
        """
        return re.sub('\s+', ' ', phrase).strip().split(" ")[0]

    with open("/etc/lirc/lircd.conf") as file_:
        lines = [a for a in file_.readlines() if a.strip()]
        res = {}
        for (x, y) in make_groups(lines, 'begin', 'end', 'remote'):
            for (x_, y_) in make_groups(lines[x:y], 'begin', 'end', 'codes'):
                for (xn, yn) in make_groups(lines[x:y], 'name', '', ''):
                    name = lines[x:y][xn:yn+2][0].replace('name', '').strip()
                    break
                res[name] = [clean(a) for a in lines[x:y][x_+1:y_]]

        return res


BUTTONS = json.dumps(read_lirc_file())
BASE_COLORS = get_base_colors(COLORS_FILE)
APP = Flask(__name__, template_folder=TEMPLATES_DIR)
Bootstrap(APP)


@APP.route('/')
def index():
    return render_template('index.html', buttons=BUTTONS,
                           color_buttons=json.dumps(BASE_COLORS.keys()))


@APP.route('/action/<remote>/<action>')
def action(remote, action_):
    """
        Executes a custom action.
    """
    result = subprocess.check_call(['irsend', 'SEND_ONCE', remote, action_])
    return json.dumps({"key": action_, 'result': result})


@APP.route('/change_color/<remote>/<color>')
def change_light(remote, color):
    """
        Change light color.

        It takes a comma-separated RGB vector [RRR, GGG, BBB] (0..255)
        and returns the closest value from the json's color vectors calculating
        its euclidean distance.

        This way we can use a generic colorpicker and return the color
        that the lamp supports

        You need to define in COLORS_FILE your remotes for this to work.
    """
    distances = []
    curr_color = tuple(map(int, color.split(',')))

    if 'remote' not in BASE_COLORS.keys():
        return ["Remote not supported"]

    colors = [tuple(color_) for color_ in BASE_COLORS['remote']]
    for color in colors:
        distances.append([color, distance.euclidean(color, curr_color)])

    distances_sorted = list(sorted(distances, key=lambda x: x[1])[0][0])
    closest = '_'.join(map(str, distances_sorted))
    res = subprocess.check_call(['irsend', 'SEND_ONCE', remote, closest])

    return json.dumps({"key": closest, 'result': res})


def main():
    """
        Run app
    """
    APP.run(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    main()
