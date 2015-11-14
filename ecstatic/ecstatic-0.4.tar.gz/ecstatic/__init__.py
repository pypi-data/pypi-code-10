import configparser
import os
import re

from flask import Flask
from flask_appconfig import AppConfig

from .frontend import frontend


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app)
    app.register_blueprint(frontend)

    @app.before_first_request
    def setup_exports():
        cfg = configparser.ConfigParser()

        for fn in app.config['EXPORTS'].split(os.pathsep):
            cfg.read(fn)

        exports = []

        # precompile
        for sect_name, sect in cfg.items():
            # ignore special sections or DEFAULT
            if sect_name.startswith('_') or sect_name == 'DEFAULT':
                continue

            if 'match' in sect:
                # match section
                pattern = re.compile(sect['match'])
                fspath = sect['fspath']
            elif 'root' in sect:
                # basic section
                pattern = re.compile(r'^(.*)$')
                fspath = sect['root'] + '/{}'
            else:
                # section has neither match nor root
                continue

            exports.append((pattern, fspath, sect))

        app.exports = exports

    return app
