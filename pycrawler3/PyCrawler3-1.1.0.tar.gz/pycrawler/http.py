import requests
from requests.exceptions import ConnectionError, MissingSchema
from http.client import OK


class HttpRequest:

    @classmethod
    def get(cls, url):

        try:
            response = requests.get(url)
        except MissingSchema:
            response = requests.get('http://{}'.format(url))
        except ConnectionError:
            return ''

        return response.text if response.status_code == OK else ''
