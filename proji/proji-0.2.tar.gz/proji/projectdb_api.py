'''
API wrapper for Centre for eResearch project database.

Links:

API doc: https://wiki.auckland.ac.nz/display/CERES/eResearch+Rest+API

'''

from restkit import Resource, BasicAuth
from projectdb_models import *
from pyclist.pyclist import API_MARKER

try:
    import simplejson as json
except ImportError:
    import json # py2.6 only



PROJECTDB_DEFAULT_URL = 'https://web.ceres.auckland.ac.nz/eresearch/api'

POSITIONAL_ARG_REGISTRY = {}


# Helper methods ========================================
def get_request_params(params={}):

    return params


def add_list_method(cls, model_type):

    def list_method(self):

        response = self.get('/'+model_type, params_dict=get_request_params(), headers=self.headers)

        result_list = json.loads(response.body_string())

        cls = eval(model_type)

        result = []
        for item in result_list:
            obj = cls(**item)
            result.append(obj)

        return result

    list_method.__doc__ = '''
        Returns a list of all {0}s.

        :return: A list of {0}s.
        :rtype: list
        '''.format(model_type)
    list_method.__name__ = 'call_list_{0}'.format(model_type)
    setattr(cls, list_method.__name__, list_method)

def add_get_method(cls, model_type):

    def get_method(self, id):

        response = self.get('/{0}/{1}'.format(model_type, id), params_dict=get_request_params(), headers=self.headers)

        result_dict = json.loads(response.body_string())

        cls  = eval(model_type)
        result = cls(**result_dict)

        return result

    get_method.__doc__ = '''
    Returns the {0} with the specified id.

    :type id: int
    :param id: the id of the {0}
    :return: the {0}
    :rtype: {0}
    '''.format(model_type)
    get_method.__name__ = 'call_get_{0}'.format(model_type)
    setattr(cls, get_method.__name__, get_method)
    pretty_method_name = get_method.__name__[len(API_MARKER)+1:]
    POSITIONAL_ARG_REGISTRY[pretty_method_name] = 'id'

def add_change_value_method(cls, model_type):

    def change_value_method(self, id, key, value):

        value_dict = {key: value}
        value_json = json.dumps(value_dict)

        response = self.put('/{0}/{1}'.format(model_type, id), headers=self.headers, payload=value_json)

        print response
        return True

    change_value_method.__doc__ = '''
    Changes one key/value pair for the {0} with the specified id.

    :type id: int
    :param id: the id of the {0}
    :type key: str
    :param key: the key
    :type value: str
    :param value: the value
    :return: whether the the setting of the value succeeded
    :rtype: bool
    '''.format(model_type)
    change_value_method.__name__ = 'call_change_value_{0}'.format(model_type)
    setattr(cls, change_value_method.__name__, change_value_method)



classes = [
        'authzRole',
        'department',
        'division',
        'externalReference',
        'facility',
        'institution',
        'institutionalRole',
        'kpiCategory',
        'kpi',
        'person',
        'personProject',
        'personProperty',
        'personRole',
        'personStatus',
        'project',
        'projectAction',
        'projectActionType',
        'projectFacility',
        'projectKpi'
    ]


# API-Wrapper classes ========================================
class projectdb_api(Resource):


    def __init__(self, username, token, url=PROJECTDB_DEFAULT_URL, **kwargs):

        self.auth = BasicAuth(username, token)
        self.base_url = url
        super(projectdb_api, self).__init__(self.base_url, filters=[self.auth])
        self.headers = {
            'Content-Type': 'application/json',
        }




# dynamically create 'list' methods
for model_type in classes:
    add_list_method(projectdb_api, model_type)
    add_get_method(projectdb_api, model_type)
    add_change_value_method(projectdb_api, model_type)
