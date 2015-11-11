__author__ = 'Hari Jiang'


class Response(object):
    def __init__(self, status=None, headers=None, body=None):
        self.status = status
        self.headers = headers
        self.body = body

    @staticmethod
    def from_requests_response(response):
        return Response(status=response.status_code, body=response.text,
                        headers=dict(response.headers))

    def __str__(self):
        return """{status}
{headers}
{body}""".format(**self.__dict__)
