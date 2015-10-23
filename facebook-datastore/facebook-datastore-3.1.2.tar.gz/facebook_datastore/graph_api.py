from facepy import graph_api

from django.conf import settings


def get_graph_api(user):
    version = getattr(settings, 'FACEBOOK_API_VERSION', '2.1')
    return GraphAPI(user.access_token, version=version)


class GraphAPI(graph_api.GraphAPI):
    def _parse(self, data):
        parsed = super(GraphAPI, self)._parse(data)
        return get_data_object(data.decode('utf-8'), parsed)


def get_data_object(raw_data, data):
    class DataType(type(data)):
        __slots__ = ('raw_data')

    result = DataType(data)
    result.raw_data = raw_data
    return result
