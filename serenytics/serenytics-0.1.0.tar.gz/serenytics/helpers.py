import logging

import requests


HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_412_PRECONDITION_FAILED = 412


def make_request(method, url,
                 error_messages=None,
                 generic_error_message=None,
                 expected_status_code=HTTP_200_OK,
                 **kwargs):
    response = requests.request(method, url, **kwargs)
    logging.debug('{method} {url} {code}'.format(method=method.upper(),
                                                 url=url,
                                                 code=response.status_code))

    if error_messages is not None and response.status_code in error_messages:
        raise SerenyticsException(error_messages[response.status_code])

    if response.status_code == HTTP_401_UNAUTHORIZED:
        raise SerenyticsException('Unauthorized: please check your API key and retry')

    if response.status_code != expected_status_code:
        logging.debug('reponse: %s' % response.text)
        raise SerenyticsException(generic_error_message or
                                  'Error while calling Serenytics API. Please retry or contact suppor@serenytics.com')

    return response


class SerenyticsException(Exception):
    """Exception launched by Serenytics Client when an error occured."""
