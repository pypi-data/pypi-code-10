"""
    flask_jsonschemer
    ~~~~~~~~~~~~~~~~

    flask_jsonschemer
"""

import os
from functools import wraps

from flask import current_app, request, json
from jsonschema import ValidationError, validate as _validate


_methods = ('POST', 'PUT', 'PATCH')


class JsonSchemer(object):
    def __init__(self, app=None, format_checker=None):
        self.app = app
        self.format_checker = format_checker
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # Load schemas
        default_path = os.path.join(app.root_path, 'schemas')
        path = app.config.get('JSONSCHEMER_DIR', default_path)
        self._schemas = load_schemas(path)

        # Set schema extension
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['jsonschemer'] = self

    def get_schema(self, path):
        schema = self._schemas[path[0]]
        for p in path[1:]:
            schema = schema[p]
        return schema


def load_schemas(path):
    schemas = {}
    for p in os.listdir(path):
        key = p.split('.')[0]
        p = os.path.join(path, p)
        if os.path.isdir(p) or not p.endswith('.json'):
            continue
        with open(p, 'r') as f:
            schemas[key] = json.load(f)
    return schemas


def validate(*path):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            methods = current_app.config.get('JSONSCHEMER_METHODS', _methods)
            jsonschemer = current_app.extensions.get('jsonschemer', None)
            if request.method not in methods:
                return fn(*args, **kwargs)
            elif jsonschemer is None:
                raise RuntimeError('Flask-JsonSchemer was not properly '
                                   'initialized for the current '
                                   'application: %s' % current_app)

            data = request.get_json(silent=True)
            schema = jsonschemer.get_schema(path)
            _validate(data, schema, format_checker=jsonschemer.format_checker)
            return fn(*args, **kwargs)
        return decorated
    return wrapper
