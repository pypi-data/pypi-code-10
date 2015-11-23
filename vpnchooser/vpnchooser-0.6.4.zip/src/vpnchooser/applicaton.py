# -*- encoding: utf-8 -*-

from flask import Flask, redirect, url_for
from flask.ext.restful import Api

from .celery import make_celery


app = Flask('vpnchooser')
api = Api(app)

celery = make_celery(app)


@app.route('/')
@app.route('/static')
@app.route('/static/')
def index_route():
    return redirect(url_for('static', filename='index.html'))
