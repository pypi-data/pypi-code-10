import json
from flask import request
from flask.ext.restful import Resource
from functools import wraps
from server.utils.AMSRESTUtils import *

def auth_me(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        result = None
        # get the session token
        session_token = request.cookies.get('ua_session_token')
        if session_token is None:
            session_token = request.values.get('ua_session_token')
        reqd = request.data

        authorized = True

        if authorized is False:
            return result, 401
        request.data = json.dumps(reqd)
        return f(*args, **kwargs)
    return decorated


class ProtectedResource(Resource):
    method_decorators = [auth_me]

def userapp_authenticate(login_str, password):
    if login_str is None or password is None:
        return None

    return login_str+password


