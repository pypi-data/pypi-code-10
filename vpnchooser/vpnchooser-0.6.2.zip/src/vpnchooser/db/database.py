# -*- encoding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy

from vpnchooser.applicaton import app

db = SQLAlchemy(app)
