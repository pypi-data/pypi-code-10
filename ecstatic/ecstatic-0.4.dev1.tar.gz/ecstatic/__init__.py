from flask import Flask
from flask_appconfig import AppConfig

from .frontend import frontend


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app)
    app.register_blueprint(frontend)

    return app
