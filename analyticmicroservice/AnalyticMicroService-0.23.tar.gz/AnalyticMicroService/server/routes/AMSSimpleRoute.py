__author__ = 'Chris Bergh'
import flask.ext
import requests, json, datetime, time
import shutil
from flask import request

from flask.ext.restful import Resource, reqparse
from server.utils.AMSUserApp import ProtectedResource

class AMSSimpleRoute(Resource):

    def get(self):
        return {'end': 'toend'}

    def put(self):
        print request.form['data']
        return {'end': 'toendput'}, 201, {'Access-Control-Allow-Origin': '*'}

    def post(self):
        try:
            parser = reqparse.RequestParser()
            input_data = request.data
            #print request.headers
            if input_data is not None:
                rv = "{end: toendpost, %s}" % input_data
            else:
                rv = "{end: toendpost}"
        except Exception:
            rv = "{end: toendpostexception}"

        return rv

    # has to be here for CORS to work
    def options(self):
        pass


class TestProtected(ProtectedResource):

    def get(self, recipeuuid):
        return {'recipe-uuid': recipeuuid}

    # has to be here for CORS to work
    def options(self):
        pass

class EndToEndProtected(ProtectedResource):
    def get(self):
        return {'end': 'toendprotected'}

    def post(self):
        try:
            parser = reqparse.RequestParser()
            input_data = request.data
            #print request.headers
            if input_data is not None:
                rv = "{'end': toendprotectedpost, %s, 'rude': %s}" % (input_data, 'rude string')
            else:
                rv = "{'end': toendpreotectedpost, 'rude': %s}" % 'rude string'
        except Exception, e:
            rv = "{'end': toendpretectedpostexcetption, 'exception': %s}" % str(e)

        return rv

    # has to be here for CORS to work
    def options(self):
        pass

