#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Flask based API.
    Requires ircsend to work.
"""

from flask import Flask, render_template, Response, request
from flask_bootstrap import Bootstrap
from functools import wraps
import subprocess
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
CONF_FILE = os.path.join("/etc/lirc/lircd.conf")


def read_lirc_file():
    """
        Reads a LIRC config file
        and extrats the remotes and buttons =)
    """

    def make_groups(lines, start, end, name):
        """        """
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
APP = Flask(__name__, template_folder=TEMPLATES_DIR)
Bootstrap(APP)


def check_auth(username, password):
    return username == 'admin' and password == 'admin'


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@APP.route('/')
@requires_auth
def index():
    return render_template('index.html', buttons=BUTTONS)


@requires_auth
@APP.route('/<remote>/<action_>')
def action(remote, action_):
    """
        Executes a custom action.
    """
    result = subprocess.check_call(['irsend', 'SEND_ONCE', remote, action_])
    return json.dumps({"key": action_, 'result': result})


def main():
    """
        Run app
    """
    APP.run(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    main()
