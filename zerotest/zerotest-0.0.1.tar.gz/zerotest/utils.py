from __future__ import print_function

__author__ = 'Hari Jiang'


def dict_to_wsgi_headers(headers):
    wsgi_headers = []
    for k, v in headers.items():
        wsgi_headers.append((k, v))

    return wsgi_headers


def response_with_response(response, start_response):
    start_response("{} {}".format(response.status_code, response.reason), dict_to_wsgi_headers(response.headers))
    return response


_DEFAULT_LINE_NOTIFY_FORMAT = '{:=^120}'


def print_line_notify(msg):
    print(_DEFAULT_LINE_NOTIFY_FORMAT.format(" {} ".format(msg)))
