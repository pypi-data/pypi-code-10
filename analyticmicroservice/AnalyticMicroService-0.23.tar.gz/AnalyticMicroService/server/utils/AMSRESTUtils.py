__author__ = 'Chris Bergh'

import urllib
from flask.ext.restful import abort
from server.utils.AMSSingletons import *
from collections import OrderedDict

class AMSRESTUtils:

    def __init__(self):
        pass

    @staticmethod
    def check_input(input_data, request_values=None, request_args=None):

        bad_data = False
        in_dict = OrderedDict()
        if input_data is None:
            bad_data = True
        else:
            try:
                in_dict = json.loads(input_data, object_pairs_hook=OrderedDict)
            except ValueError:
                bad_data = True

        request_args_dict = OrderedDict()
        if request_args is not None:
            if isinstance(request_args, dict) is True:
                for k, v in request_args.iteritems():
                    if isinstance(v, basestring) is True:
                        v2 = None
                        try:
                            v2 = json.loads(v, object_pairs_hook=OrderedDict)
                        except Exception:
                            v2 = v
                        request_args_dict[k] = v2
                    else:
                        request_args_dict[k] = v

        for k, v in request_args_dict.iteritems():
            in_dict[k] = v

        if bad_data is True:
            return None
        else:
            if request_values is not None and len(request_values) > 0:
                for k, v in request_values.iteritems():
                    in_dict[k] = v
            return in_dict

    @staticmethod
    def url_encode(url_string):
        return urllib.quote_plus(url_string)

    @staticmethod
    def set_success(return_dl):
        if return_dl is None:
            pass
        elif isinstance(return_dl, list):
            pass
        elif isinstance(return_dl, dict):
            return_dl['status'] = 'success'

    @staticmethod
    def set_failure(return_dl, error_message):
        if return_dl is None:
            pass
        elif isinstance(return_dl, list):
            pass
        elif isinstance(return_dl, dict):
            return_dl['status'] = 'failed'
            return_dl['error'] = error_message

    @staticmethod
    def complete_response(return_dl):
        if return_dl is None:
            abort(404, message="AMSServer: not found")
        else:
            return_json = None
            try:
                rj = json.dumps(return_dl)
                return_json = rj #.replace("\\n", "").replace("\\", "").replace("\"{", "{").replace("}\"", "}").replace("\"[", "[").replace("]\"", "]")
            except ValueError:
                return_dict = dict()
                AMSRESTUtils.set_failure(return_dict, 'bad output data')
                return_json = json.dumps(return_dict)
            finally:
                if isinstance(return_dl, list):
                    return return_json
                elif isinstance(return_dl, dict) and ('status' in return_dl and return_dl['status'] != 'success'):
                    abort(400, message="\%s" % return_json)
                else:
                    return return_json

    @staticmethod
    def convert(the_input):
        return AMSHelpers.convert(the_input)

    @staticmethod
    def split_one(path):
        return AMSHelpers().split_one(path)

    @staticmethod
    def split_one_end(path):
        return AMSHelpers().split_one_end(path)

    @staticmethod
    def decode_list(data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = AMSRESTUtils.decode_list(item)
            elif isinstance(item, dict):
                item = AMSRESTUtils.decode_dict(item)
            rv.append(item)
        return rv

    @staticmethod
    def decode_dict(data):
        rv = OrderedDict()
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = AMSRESTUtils.decode_list(value)
            elif isinstance(value, dict):
                value = AMSRESTUtils.decode_dict(value)
            rv[key] = value
        return rv
