import json
from requests import Session
from shushuo import response


class ShushuoApi(object):
    """
    Used by the client to communicate to the shushuo API.
    """

    def __init__(self, project_id, project_key,
                 endpoint_url=None,
                 post_timeout=None,
                 get_timeout=None):
        self._project_id = project_id
        self._project_key = project_key
        self._session = self._create_session()

        if post_timeout is not None:
            self._post_timeout = post_timeout
        else:
            self._post_timeout = 60

        if get_timeout is not None:
            self._get_timeout = get_timeout
        else:
            self._get_timeout = 60

        if endpoint_url is not None:
            self._endpoint_url = endpoint_url
        else:
            self._endpoint_url = "https://api.shushuo.com"

    def _create_session(self):
        s = Session()
        s.headers.update({
            "Content-Type": "application/json",
            "X-Project-Key": self._project_key,
            "X-Project-Id": self._project_id
        })
        return s

    def post_event(self, collection_name, event):
        url = "{0}/events/{1}".format(self._endpoint_url, collection_name)
        payload = json.dumps(event)

        return self._request(url=url,
                             method='post',
                             payload=payload)

    def post_events(self, events):
        url = "{0}/events".format(self._endpoint_url)
        payload = json.dumps(events)

        return self._request(url=url,
                             method='post',
                             payload=payload)

    def post_profile(self, collection_name, profile):
        url = "{0}/profiles/{1}".format(self._endpoint_url, collection_name)
        payload = json.dumps(profile)

        return self._request(url=url,
                             method='post',
                             payload=payload)

    def query_events(self, collection_name, query_body):
        url = "{0}/events/{1}".format(self._endpoint_url, collection_name)
        payload = {
            'query': json.dumps(query_body)
        }

        return self._request(url=url,
                             method='get',
                             payload=payload)

    def _request(self, url, method, payload):
        try:
            if method == 'get':
                r = self._session.get(url=url,
                                      params=payload,
                                      timeout=self._get_timeout)
            elif method == 'post':
                r = self._session.post(url=url,
                                       data=payload,
                                       timeout=self._post_timeout)
            else:
                raise Exception('Not support other method.')
        except Exception as ex:
            return response.ShushuoResponse(
                status_code=-1,
                error_message='Unknow issue %s' % ex,
                result=None)

        return self._build_response(r)

    def _build_response(self, r):
        try:
            result = r.json()
        except ValueError:
            result = {
                'error_code': r.status_code,
                'message': r.text
            }

        error_message = None
        if r.status_code == 403:
            error_message = "Unauthorised. Plz check your Project Id and Key"
        elif r.status_code != 200:
            error_message = result.get('message', 'Unknow issue.')

        return response.ShushuoResponse(status_code=r.status_code,
                                        error_message=error_message,
                                        result=result)
