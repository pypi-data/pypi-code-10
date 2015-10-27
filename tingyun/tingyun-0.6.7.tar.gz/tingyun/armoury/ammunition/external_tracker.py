
"""

"""

import logging

from tingyun.armoury.ammunition.timer import Timer
from tingyun.logistics.warehouse.external_node import ExternalNode
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.logistics.basic_wrapper import FunctionWrapper, wrap_object

console = logging.getLogger(__name__)


class ExternalTrace(Timer):
    """define the external trace common api.

    """
    def __init__(self, tracker, library, url, params=None):
        super(ExternalTrace, self).__init__(tracker)

        self.library = library
        self.url = url.split('?')[0]
        self.params = self.parse_request_params(url, params)

        signed_param = []
        for p in self.params:
            if tracker.settings and p in tracker.settings.external_url_params_captured.get(self.url, ""):
                signed_param.append("%s=%s&" % (p, self.params[p]))

        if 0 != len(signed_param):
            self.url = "%s?%s" % (self.url, ''.join(signed_param).rstrip('&'))

    def parse_request_params(self, url, post_data):
        """ Note: some url request lib passed in the post data in different way.
        so do not support post data params capture now.
        :param url:
        :param post_data:
        :return:
        """
        url_params = url.split("?")
        list_params = url_params[1] if 2 == len(url_params) else ""
        get_params = dict([tuple(p.split('=')) for p in list_params.split("&") if p])

        return get_params

    def create_node(self):
        return ExternalNode(library=self.library, url=self.url, children=self.children,
                            start_time=self.start_time, end_time=self.end_time, duration=self.duration,
                            exclusive=self.exclusive)

    def terminal_node(self):
        return True


def external_trace_wrapper(wrapped, library, url):

    def dynamic_wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()
        if tracker is None:
            return wrapped(*args, **kwargs)

        _url = url
        if callable(url):
            if instance is not None:
                _url = url(instance, *args, **kwargs)
            else:
                _url = url(*args, **kwargs)

        with ExternalTrace(tracker, library, _url, kwargs):
            return wrapped(*args, **kwargs)

    def literal_wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()

        if tracker is None:
            return wrapped(*args, **kwargs)

        with ExternalTrace(tracker, library, url, kwargs):
            return wrapped(*args, **kwargs)

    if callable(url):
        return FunctionWrapper(wrapped, dynamic_wrapper)

    return FunctionWrapper(wrapped, literal_wrapper)


def wrap_external_trace(module, object_path, library, url):
    wrap_object(module, object_path, external_trace_wrapper, (library, url))
