import json

from .helpers import SerenyticsException, make_request, HTTP_412_PRECONDITION_FAILED
from . import settings


class DataSource(object):
    """
    Serenytics data source
    """

    def __init__(self, config, headers):
        self._config = config
        self._headers = headers

    @property
    def name(self):
        return self._config['name']

    @property
    def uuid(self):
        return self._config['uuid']

    def reload_data(self, new_data):
        """
        Reset data of a Push data source.

        It erases old data and loads new data instead.

        Notes:
            - current data source must be a Push data source
            - new data doesn't have to have the same structure as old data.
        """
        if self._config['type'] != 'Push':
            raise SerenyticsException('Error: You can only reload the data of a push data source.')

        push_url = self._config['jsonContent']['url']
        reload_url = push_url.replace('/push/', '/reload/')
        make_request('post', reload_url, data=json.dumps(new_data), headers={'Content-type': 'application/json'})

    def get_data(self, options=None):
        """
        Extract data from the data source
        """
        no_options = options is None

        if no_options:
            options = {
                'format': 'simple_array',
                'only_headers': True
            }

        response = make_request('post', settings.SERENYTICS_API_DOMAIN + '/api/formatted_data/' + self.uuid,
                                error_messages={HTTP_412_PRECONDITION_FAILED: 'Invalid options'},
                                data=json.dumps(options),
                                headers=self._headers)

        if not no_options:
            return response.json()

        # make second API call to retrieve actual data
        headers = response.json()['columns_titles']
        new_options = {
            'format': 'simple_array',
            'order': 'row_by_row',
            'data_processing_pipeline': [{
                'select': [header['name'] for header in headers]
            }]
        }
        response = make_request('post', settings.SERENYTICS_API_DOMAIN + '/api/formatted_data/' + self.uuid,
                                error_messages={HTTP_412_PRECONDITION_FAILED: 'Invalid options'},
                                data=json.dumps(new_options),
                                headers=self._headers)

        return response.json()
