from copy import copy


def dict_to_wsgi_headers(headers):
    wsgi_headers = []
    for k, v in headers.items():
        wsgi_headers.append((k, v))

    return wsgi_headers


def response_with_response(response, start_response):
    headers = copy(response.headers)
    # remove transfer encoding
    for k in ('Content-Encoding', 'Transfer-Encoding'):
        headers.pop(k, None)
    start_response("{} {}".format(response.status_code, response.reason), dict_to_wsgi_headers(headers))
    return response
