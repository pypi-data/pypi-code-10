"""
Module containing the main class that create the post data and makes the HTTP
request according to the ATLAS API.
"""

import calendar
import requests
from dateutil import parser
from datetime import datetime

from .version import __version__


class AtlasRequest(object):
    """
    Base class for doing Atlas requests. Contains functions that can be used by
    most Atlas requests.
    """

    http_methods = {
        "GET": requests.get,
        "POST": requests.post,
        "DELETE": requests.delete
    }

    def __init__(self, **kwargs):
        self.url = ""
        self.url_path = ""
        self.key = kwargs.get("key", "")
        if "url_path" in kwargs:
            self.url_path = kwargs["url_path"]
        if "server" in kwargs:
            self.server = kwargs["server"]
        else:
            self.server = "atlas.ripe.net"

        self.http_agent = "RIPE ATLAS Cousteau v{0}".format(__version__)

        self.http_method_args = {
            "params": {"key": self.key},
            "headers": self.get_headers()
        }
        self.post_data = {}

    def get_headers(self):
        """Return header for the HTTP request."""
        return {
            "User-Agent": self.http_agent,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def http_method(self, method):
        """
        Execute the given HTTP method and returns if it's success or not
        and the response as a string if not success and as python object after
        unjson if it's success.
        """
        return_json_methods = ["GET", "POST"]
        self.build_url()

        try:
            response = self.get_http_method(method)
            is_success = response.ok
            if is_success and method in return_json_methods:
                response_message = response.json()
            else:
                response_message = response.text
        except requests.exceptions.RequestException as exc:
            is_success = False
            response_message = exc.args

        return is_success, response_message

    def get_http_method(self, method):
        """Gets the http method that will be called from the requests library"""
        return self.http_methods[method](self.url, **self.http_method_args)

    def build_url(self):
        """
        Builds the request's url combining server and url_path
        classes attributes.
        """
        self.url = "https://{0}{1}".format(self.server, self.url_path)

    def get(self, **url_params):
        """
        Makes the HTTP GET to the url.
        """
        if url_params:
            self.http_method_args["params"].update(url_params)
        return self.http_method("GET")

    def post(self):
        """
        Makes the HTTP POST to the url sending post_data.
        """
        self._construct_post_data()

        post_args = {"json": self.post_data}
        self.http_method_args.update(post_args)

        return self.http_method("POST")

    def _construct_post_data(self):
        raise NotImplementedError


class AtlasCreateRequest(AtlasRequest):
    """
    Class responsible for creating a request for creating a new Atlas
    measurement. Takes as arguments Atlas API key, a list of Atlas measurement
    objects and a list of Atlas sources. Optionally the start and end time and
    whether the measurement is a oneoff can be specified.
    Usage:
        from ripe.atlas import AtlasCreateRequest
        ar = AtlasCreateRequest(**{
            "start_time": start,
            "stop_time": stop,
            "key": "path_to_key",
            "measurements":[measurement1, ...],
            "sources": [source1, ...],
            "is_oneoff": True/False
        })
        ar.create()
    """

    def __init__(self, **kwargs):
        super(AtlasCreateRequest, self).__init__(**kwargs)

        self.url_path = '/api/v2/measurements/'

        self.measurements = kwargs["measurements"]
        self.sources = kwargs["sources"]
        if kwargs.get("start_time"):
            self.start_time = kwargs["start_time"]
        else:
            self.start_time = ""
        if kwargs.get("stop_time"):
            self.stop_time = kwargs["stop_time"]
        else:
            self.stop_time = ""
        if kwargs.get("is_oneoff"):
            self.is_oneoff = kwargs["is_oneoff"]
        else:
            self.is_oneoff = False

    def _construct_post_data(self):
        """
        Constructs the data structure that is required from the atlas API based
        on measurements, sources and times user has specified.
        """
        definitions = [msm.build_api_struct() for msm in self.measurements]
        probes = [source.build_api_struct() for source in self.sources]
        self.post_data = {
            "definitions": definitions,
            "probes": probes,
            "is_oneoff": self.is_oneoff
        }
        if self.start_time:
            self.post_data.update(
                {"start_time": int(calendar.timegm(self.start_time.timetuple()))}
            )
        if self.stop_time:
            self.post_data.update(
                {"stop_time": int(calendar.timegm(self.stop_time.timetuple()))}
            )

    def create(self):
        """Sends the POST request"""
        return self.post()


class AtlasChangeRequest(AtlasRequest):
    """Atlas request for changing probes for a running measurement.
    post_data = [{
        "action": "add|remove",
        "requested": probe_number,
        # when action=remove only probes is supported
        "type": "area|country|asn|prefix|msm|probes",
        "value": probe_values
    }]
    """

    def __init__(self, **kwargs):
        super(AtlasChangeRequest, self).__init__(**kwargs)

        self.url_path = '/api/v2/measurements/{0}/participation-requests/'
        self.msm_id = kwargs["msm_id"]
        self.sources = kwargs["sources"]
        self.url_path = self.url_path.format(self.msm_id)

    def _construct_post_data(self):
        """
        Constructs the data structure that is required from the atlas API based
        on measurement id, and the sources.
        """
        self.post_data = [source.build_api_struct() for source in self.sources]

    def create(self):
        """Sends the POST request"""
        return self.post()


class AtlasStopRequest(AtlasRequest):
    """Atlas request for stopping a measurement."""

    def __init__(self, **kwargs):
        super(AtlasStopRequest, self).__init__(**kwargs)

        self.url_path = '/api/v2/measurements/'
        self.msm_id = kwargs["msm_id"]
        self.url_path = "{0}{1}".format(self.url_path, self.msm_id)

    def delete(self):
        """
        Makes the HTTP DELETE to the url.
        """
        return self.http_method("DELETE")

    def create(self):
        """Sends the DELETE request"""
        return self.delete()


class AtlasLatestRequest(AtlasRequest):

    def __init__(self, msm_id=None, probe_ids=(), **kwargs):
        super(AtlasLatestRequest, self).__init__(**kwargs)

        self.url_path = "/api/v2/measurements/{0}/latest"

        self.msm_id = msm_id
        self.probe_ids = probe_ids

        self.url_path = self.url_path.format(self.msm_id)
        if self.probe_ids:
            additional_params = {
                "probe_ids": ",".join(map(str, self.probe_ids))
            }

            self.http_method_args["params"].update(additional_params)


class AtlasResultsRequest(AtlasRequest):
    """Atlas request for fetching results of a measurement."""

    def __init__(self, **kwargs):
        super(AtlasResultsRequest, self).__init__(**kwargs)

        self.url_path = '/api/v2/measurements/{0}/results'
        self.msm_id = kwargs["msm_id"]
        start = kwargs.get("start")
        stop = kwargs.get("stop")
        self.probe_ids = kwargs.get("probe_ids")

        self.start = None
        self.stop = None
        self.clean_start_time(start)
        self.clean_stop_time(stop)

        self.url_path = self.url_path.format(self.msm_id)

        self.update_http_method_params()

    def clean_start_time(self, start):
        """
        Transform start time filter to datetime object if there is any.
        """
        if isinstance(start, datetime):
            self.start = start
        elif isinstance(start, int):
            self.start = datetime.utcfromtimestamp(start)
        elif isinstance(start, str):
            self.start = parser.parse(start)

    def clean_stop_time(self, stop):
        """
        Transform stop time filter to datetime object if there is any.
        """
        if isinstance(stop, datetime):
            self.stop = stop
        elif isinstance(stop, int):
            self.stop = datetime.utcfromtimestamp(stop)
        elif isinstance(stop, str):
            self.stop = parser.parse(stop)

    def update_http_method_params(self):
        """
        Update HTTP url parameters based on msm_id and query filters if
        there are any.
        """
        url_params = {}

        if self.start:
            url_params.update(
                {"start": int(calendar.timegm(self.start.timetuple()))}
            )

        if self.stop:
            url_params.update(
                {"stop": int(calendar.timegm(self.stop.timetuple()))}
            )

        if self.probe_ids:
            url_params.update({"probe_ids": ",".join(map(str, self.probe_ids))})

        self.http_method_args["params"].update(url_params)

    def create(self):
        """Sends the GET request."""
        return self.get()


__all__ = [
    "AtlasStopRequest", "AtlasCreateRequest",
    "AtlasChangeRequest", "AtlasRequest",
    "AtlasResultsRequest"
]
