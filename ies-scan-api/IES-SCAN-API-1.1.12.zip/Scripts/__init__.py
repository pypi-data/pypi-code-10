import json
from urllib.parse import urljoin
from urllib.request import urlopen, Request 

def expand_url(url,args):
    for k,v in args.items():
        url = url.replace('{' + k + '}', str(v))
    return url


# the API token is created for a specific project and allows a script to
# impersonate that user.  see 'API tokens' under the project menu
#
# set the base URL of the project the token is for, obtained from the
# link at the bottom of the project's 'API tokens' page.
# e.g.  BASE_URL = 'https://scan.iseve.com/project/ApiTestProject'
#
# root = open_api(BASE_URL, API_TOKEN)
#
# get and post helpers for JSON and raw data, inserting the bearer token into
# the Authorization header
class Api(object):
    def __init__(self, base_url, api_token):
        self._base_url = base_url
        self._api_token = api_token

    def root(self): 
        """GET the api object for the base URL of the project"""
        req = Request(self._base_url)
        req.add_header('Authorization', 'Bearer ' + self._api_token)
        res = urlopen(req)
        return ApiObject(self, json.loads(res.read().decode(res.info().get_param('charset') or 'utf-8')))

    def get_json(self, url, **kwargs):
        """GET the url relative to the base url and return a dict populated from the returned json"""
        url = expand_url(url,kwargs)
        req = Request(urljoin(self._base_url, url))
        req.add_header('Authorization', 'Bearer ' + self._api_token)
        res = urlopen(req)
        return json.loads(res.read().decode(res.info().get_param('charset') or 'utf-8'))
    
    def _get_object(self, url, **kwargs):
        return self._to_object(self.get_json(url, **kwargs))
    
    def _post_object(self, url, data, **kwargs):
        return self._to_object(self.post_json(url, data, **kwargs))

    def _to_object(self, json):
        if 'Error' in json:
            raise ApiError(self, json['Message'])
        return ApiObject(self, json)
    
    def get_raw(self, url, **kwargs):
        """GET the url relative to the base url and return the response"""
        url = expand_url(url, kwargs)
        req = Request(urljoin(self._base_url, url))
        req.add_header('Authorization', 'Bearer ' + self._api_token)
        return urlopen(req)
    
    def post_json(self, url, data, **kwargs):
        """POST the given data to the url relative to the base url and return a dict populated from the returned json"""
        url = expand_url(url, kwargs)
        req = Request(urljoin(self._base_url, url), json.dumps(data).encode('utf-8'))
        req.add_header('Authorization', 'Bearer ' + self._api_token)
        req.add_header('Content-Type', 'application/json')
        res = urlopen(req)
        return json.loads(res.read().decode(res.info().get_param('charset') or 'utf-8'))

    def post_raw(self, url, data):
        """POST the given data to the url relative to the base url and return the response"""
        req = Request(urljoin(self._base_url, url), json.dumps(data).encode('utf-8'))
        req.add_header('Authorization', 'Bearer ' + self._api_token)
        req.add_header('Content-Type', 'application/json')
        return urlopen(req)

def convert_recurse(api, data):
    return ApiObject(api, data) if type(data) is dict else data

class ApiError(Exception):
    def __init__(self, source, message):
        self.source = source
        self.message = message
    def __str__(self):
        return repr(self.message)

class ApiObject(object):
    """Wraps the endpoints in the json API as actions on objects and their properties."""
    def __str__(self):
        name = self.DisplayName if 'DisplayName' in self.__dict__ else '?'
        item = self.ItemName if 'ItemName' in self.__dict__ else '?'
        link = self._links['details']['href'] if 'details' in self._links else '?'
        return '{0} [{1}] @ {2}'.format(name, item, link) 

    def __init__(self, api, parms):
        self._api = api

        if ('_links' in parms):
            self._links = parms['_links']
            parms.pop('_links', None)
        else:
            self._links = {}

        for k,v in parms.items():
            if type(v) is dict:
                parms[k] = ApiObject(api, v)
            elif type(v) is list:
                parms[k] = [ convert_recurse(api, item) for item in v]
                
        self.__dict__.update(parms)

    def get(self, relation, **kwargs):
        """GET the related url for the object and return an ApiObject populated from the returned json"""
        return self._api._get_object(self._links[relation]['href'], **kwargs)

    def get_raw(self, relation, **kwargs):
        """GET the related url for the object and return an ApiObject populated from the returned json"""
        return self._api.get_raw(self._links[relation]['href'], **kwargs)

    def post(self, relation, data, **kwargs):
        """POST the data to the related url for the object and return an ApiObject populated from the returned json. Data may be dict, list, primitve or ApiObject"""
        return self._api._post_object(self._links[relation]['href'], data.to_data() if data is ApiObject else data, **kwargs)

    def refresh(self):
        """Fetch the object's data again via its 'details' link"""
        old_links = self._links
        self.__dict__.update(self._api.get_json(self._links['details']['href']))
        old_links.update(self._links)
        self._links = old_links
        return self

    def update(self):
        """Saves any changes made to the object by post the object's data to its 'update' link"""
        update = self._api.post_json(self._links['update']['href'], self.to_data())
        if 'Error' in update:
            raise ApiError(self, update['Message'])
        self.__dict__.update(update)
        return self

    def to_data(self):
        """Convert to a dict, omitting the _links field"""
        d = dict(self.__dict__)
        if '_links' in d: d.pop('_links', None)
        if '_api' in d: d.pop('_api', None)

        for k,v in d.items():
            if v is ApiObject:
                d[k] = v.to_data()

        return d

def open_api(base_url, api_token):
    return Api(base_url, api_token).root()