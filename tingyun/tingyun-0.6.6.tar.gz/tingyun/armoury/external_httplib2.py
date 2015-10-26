
"""this module is defined to detect the httplib2 module
"""

from tingyun.armoury.ammunition.external_tracker import wrap_external_trace


def detect_httplib2_http(module):
    """
    :param module:
    :return:
    """
    def http_url(instance, uri, method, *args, **kwargs):
        """
        :param instance:Http() instance
        :param uri:
        :param method:
        :param args:
        :param kwargs:
        :return:
        """
        return uri

    return wrap_external_trace(module, "Http.request", 'httplib2', http_url)


def detect_http_connect_with_timeout(module):
    """
    :param module:
    :return:
    """
    def http_with_timeout_url(instance, *args, **kwargs):
        """
        :param instance: HTTPConnectionWithTimeout instance
        :param args:
        :param kwargs:
        :return:
        """
        url = "http://%s" % instance.host
        if instance.port:
            url = 'http://%s:%s' % (instance.host, instance.port)

        return url

    wrap_external_trace(module, "HTTPConnectionWithTimeout.connect", 'httplib2', http_with_timeout_url)


def detect_https_connect_with_timeout(module):
    """
    :param module:
    :return:
    """
    def https_with_timeout_url(instance, *args, **kwargs):
        """
        :param instance: HTTPSConnectionWithTimeout instance
        :param args:
        :param kwargs:
        :return:
        """
        url = "http://%s" % instance.host
        if instance.port:
            url = 'http://%s:%s' % (instance.host, instance.port)

        return url

    wrap_external_trace(module, "HTTPSConnectionWithTimeout.connect", 'httplib2', https_with_timeout_url)
