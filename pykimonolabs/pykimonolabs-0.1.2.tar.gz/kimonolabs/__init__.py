import json

try:
    import urllib.request
    request = urllib.request
    import urllib
    urlencode = urllib.parse.urlencode
    python_version = 3
except:
    import urllib
    request = urllib
    urlencode = urllib.urlencode
    python_version = 2

BASE_URL = "https://www.kimonolabs.com/api"

class Kimono(object):
    def __init__(self, api_id, kimmodify=False, api_key=None, api_token=None):
        self.api_id = api_id
        self.api_key = api_key
        self.api_token = api_token
        self.kimmodify = kimmodify

    @property
    def api_url(self, query_params={}):
        if self.kimmodify:
            query_params['kimmodify'] = 1
        if self.api_key:
            query_params['apikey'] = self.api_key
        return "%s/%s/?%s" % (BASE_URL, self.api_id, urlencode(query_params))

    def fetch(self):
        data = request.urlopen(self.api_url)
        results = json.loads(data.read().decode('utf-8')) 
        return results

    @property
    def data(self):
        return self.fetch()
