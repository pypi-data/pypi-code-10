import requests
from requests.exceptions import ConnectionError, MissingSchema
from http.client import OK


class UrlNotValidException(ConnectionError):
    pass


class HttpRequest:

    @classmethod
    def get(cls, url):

        try:
            response = requests.get(url)
        except MissingSchema:
            response = requests.get('http://{}'.format(url))
        except ConnectionError:
            raise UrlNotValidException('Your page url is not valid bro!')

        return response.text if response.status_code == OK else ''
