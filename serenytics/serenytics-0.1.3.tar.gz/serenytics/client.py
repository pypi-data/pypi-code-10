import cPickle
import json
from base64 import b64encode

from serenytics.source import DataSource
from .helpers import SerenyticsException, make_request, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from . import settings


def _init_headers(api_key):
    token = 'token:' + api_key
    return {
        'Authorization': 'Basic ' + b64encode(token),
        'Content-type': 'application/json'
    }


class Client(object):
    """
    Main wrapper around Serenytics API
    """

    def __init__(self, api_key, script_id):
        self._script_id = script_id
        self._headers = _init_headers(api_key)

    def get_data_souce_by_uuid(self, uuid):
        """
        Fetch a data source by uuid

        :param uuid: string
        :return: DataSource instance
        """
        data_source_url = settings.SERENYTICS_API_DOMAIN + '/api/data_source/' + uuid
        response = make_request('get', data_source_url,
                                error_messages={HTTP_404_NOT_FOUND: 'Source with uuid "%s" does not exist' % uuid},
                                headers=self._headers)
        return DataSource(response.json(), self._headers)

    def get_or_create_push_data_source_by_name(self, name):
        """
        Retrieve the data source whose name is `name` or create a new one.

        :param name: string
        :return: DataSource instance
        """
        data_source_url = settings.SERENYTICS_API_DOMAIN + '/api/data_source'
        params = {'q': json.dumps({'filters': [{'name': 'name', 'op': 'eq', 'val': name}]})}
        response = make_request('get', data_source_url,
                                params=params,
                                headers=self._headers)

        sources = response.json()

        if sources['num_results'] == 1:
            source = sources['objects'][0]

        elif sources['num_results'] > 1:
            raise SerenyticsException('There are multiple sources named "%s". Please rename other sources.' % name)

        else:
            response = make_request('post', data_source_url,
                                    data=json.dumps({'name': name, 'type': 'Push', 'jsonContent': {}}),
                                    expected_status_code=HTTP_201_CREATED,
                                    headers=self._headers)
            source = response.json()

        return DataSource(source, self._headers)

    @property
    def _script_storage_url(self):
        return settings.SERENYTICS_API_DOMAIN + '/api/script/' + self._script_id + '/storage'

    def store_script_data(self, data):
        """
        Store script data to be retrieved during next execution of the script.

        :param data: any python object that can be pickled
        """
        make_request('put', self._script_storage_url, data=cPickle.dumps(data), headers=self._headers)

    def retrieve_script_data(self):
        """
        Retrieve script data saved in previous script execution.
        """
        response = make_request('get', self._script_storage_url, headers=self._headers)
        try:
            return cPickle.loads(response._content)
        except Exception:
            return None
