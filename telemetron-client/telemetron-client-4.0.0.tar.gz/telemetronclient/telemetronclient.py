"""
Telemetron client module.
"""

import socket
import time
import random

import certifi
import urllib3

from .utils.deepdict import DeepDict
from .utils.map import Map
from .utils.dryrunner import DryRunnerHandler
from .exceptions import TransportNotInitialized
from .exceptions import TelemetronValueError
from .defaults import METHOD_DEFAULTS
from .defaults import DEFAULT_SETTINGS


def api_client_user_agent():
    """
    Returns the string of User-Agent to use in api calls.
    """

    from . import __version__

    return 'Telemetron-client-python/%s' % (__version__,)


def make_line(prefix, name, value, tags, agg, agg_freq,
              sample_rate, namespace, timestamp):
    """
    Generate a metric line

    Keyword arguments:
    prefix -- metric prefix
    name -- Name metric such as "response_time"
    tags -- Tags to associate this value with, for example
    {from: 'serviceA', to: 'serviceB', method: 'login'}
    value
    agg -- List of aggregations to be applied by the Telemetron.
    Ex: ['avg', 'p90', 'min']
    agg_freq -- Aggregation frequency in seconds. One of: 10, 15, 30,
    60 or 300
    sample_rate -- Sampling rate (1-99)
    timestamp -- is the timestamp associated with the metric. If not
    set, will use current time (utc)

    Returns metric line string
    """

    def concat(prev, tag):
        """ concat function to be used with reduce() """
        return "%s,%s=%s" % (prev, tag, tags[tag])

    metric_name = "%s.%s.%s" % (prefix, namespace, name)
    line = reduce(concat, tags, metric_name)
    line += " %s %d" % (value, timestamp)

    if len(agg) > 0 and agg_freq:
        agg_copy = list(agg)
        agg_copy.append(agg_freq)
        line += " %s" % (','.join([str(a) for a in agg_copy]),)
        if sample_rate:
            line += " %s" % (sample_rate,)

    return line


class TelemetronClient(object):
    """
    This class represents the telemetron Client.
    It handles the socket connection to a telemetron server and has the
    ability to construct metric lines.
    """

    TRANSPORT_TCP = 'tcp'
    TRANSPORT_UDP = 'udp'
    TRANSPORT_API = 'api'
    TRANSPORT_API_SSL = 'api+ssl'

    VALID_TRANSPORTS = (
        TRANSPORT_TCP,
        TRANSPORT_UDP,
        TRANSPORT_API,
        TRANSPORT_API_SSL
        )

    API_PATH = '/tel/v2.0/metrics'

    def __init__(self, settings, defaults=None, system_stats=False):
        """
        Constructor.

        Keyword arguments:
        settings -- a dict with the following options:
            host [optional] [default: '127.0.0.1']
            port [optional] [default: 2013]
            prefix [required] - global metrics prefix
            transport [required] [one of: udp, tcp, http]
            secure [optional] [default: true] - enable or disable https
            timeout [optional] [default: 2000] - timeout for http/tcp
                                                 transports
            token [optional]
            app [optional] - if specified set a tag 'app=foo'
            dryrun [optional] [default: false] - do not actually send metrics
                                                 when flushing the buffer
            logger [optional] - logger object which supports at
                                debug/error methods
            tags [optional] [default: {}] - global list of tags to set
            sample_rate [optional] [default: 100] [between: 1-100] -
                global rate sampling
            flush_size (flush_interval) [optional] [default: 10] -
                defines the periodicity of buffer flushes
        defaults -- Default tag/aggregation definitions should be allowed on
            a per method/type basis on the client initialization - this
            should be merged first with the global tags/aggregation list
            before merging with user defined tags/aggregations per method:
            defaults [optional]
                timer [optional]
                    tags [default: see the methods description below]
                    aggregations [default: see the methods description below]
                    aggregation_frequency [default: see the methods description
                                           below]
                counter [optional]
                ...

        """

        self._settings = Map(DEFAULT_SETTINGS)
        self._settings.update(settings)
        self.global_tags = dict(self._settings.tags)
        self.global_tags.update({
            'client': api_client_user_agent()
        })
        if self._settings.app:
            self.global_tags['app'] = self._settings.app

        # Look for missing settings
        required_settings = ['prefix', 'transport']
        for prop in required_settings:
            if prop not in self._settings or \
                    not self._settings[prop]:
                raise TelemetronValueError("Missing setting '%s'" % (prop,))

        self._defaults = Map(
            DeepDict.deep_merge(
                METHOD_DEFAULTS,
                defaults or {}
                )
            )
        self.system_stats = system_stats
        self.log = self._settings.logger

        srate = self._settings.sample_rate
        if srate is not None and (srate < 1 or srate > 100):
            raise TelemetronValueError("Sample rate out of range")

        self._buffer = []
        self._socket = None
        self._pool = None

        tsp = self._settings.transport
        if tsp.lower() not in TelemetronClient.VALID_TRANSPORTS:
            raise TelemetronValueError("Invalid transport")

        self.init_transport()

        self._flush_fail_count = 0

    def transport_initialized(self):
        """
        Return True if transport was already initialized, False otherwise.
        """

        return self._socket is not None or self._pool is not None

    def init_transport(self):
        """
        Do whatever is necessary to initialize the transport.

        In case of:
        TCP - connect to endpoint
        UDP - just open the socket
        API - initialize an http(s) connection pool
        """

        if self._settings.dryrun:
            self._socket = DryRunnerHandler()
            self._pool = DryRunnerHandler()
            return

        self.log.info("Initializing transport %s", self._settings.transport)

        if self._settings.transport.lower() == self.TRANSPORT_TCP:
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
            self._socket.connect((self._settings.host, self._settings.port))
        elif self._settings.transport.lower() == self.TRANSPORT_UDP:
            if self._socket is None:
                self._socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_DGRAM)
        elif self._settings.transport.lower() == self.TRANSPORT_API:
            self._pool = urllib3.HTTPConnectionPool(
                self._settings.host,
                port=self._settings.port,
                maxsize=1,
                retries=False
                )
        elif self._settings.transport.lower() == self.TRANSPORT_API_SSL:
            self._pool = urllib3.HTTPSConnectionPool(
                self._settings.host,
                port=self._settings.port,
                maxsize=1,
                cert_reqs='CERT_REQUIRED',  # Force certificate check.
                ca_certs=certifi.where(),  # Path to the Certifi bundle.
                retries=False
                )

    def end_transport(self):
        """
        Clean up needed resources allocated by the current transport method.
        """

        self.log.debug("Cleaning up transport %s", self._settings.transport)

        if self._socket is not None:
            self._socket.close()

    def timer(self, name, value, options=None):
        """
        Sends a timing metric

        Keyword arguments:
        @param name [String] Name of the timer
        @param value [Numeric] Value of the metric
        @param [Hash] options The options to apply to the metric
        @option options [Hash] :tags Tags to associate to the metric
        @option options [Array<String>] :agg List of aggregations to be
            applied by the Telemetron
        @option options [Integer] :agg_freq Aggregation frequency in seconds
        @option options [String] :namespace Namespace of the metric
        @option options [Integer] :timestamp Timestamp of the metric
        """

        options_ = Map(
            DeepDict.deep_merge(
                {'tags': self.global_tags,
                 'namespace': self._settings.namespace},
                self._defaults['timer'],
                options or {}
                )
            )

        self.put(
            'timer.%s' % (name,),
            value or 0,
            options_.tags,
            options_.agg,
            options_.agg_freq,
            self._settings.sample_rate,
            options_.namespace,
            options_.timestamp
            )

    def counter(self, name, value, options=None):
        """
        Increments a counter

        Keyword arguments:
        @param name [String] Name of the counter
        @param value [Numeric] Increment/Decrement value, this will be
            truncated with `to_int`
        @param [Hash] options The options to apply to the metric
        @option options [Hash] :tags Tags to associate to the metric
        @option options [Array<String>] :agg List of aggregations to be
            applied by the Telemetron
        @option options [Integer] :agg_freq Aggregation frequency in seconds
        @option options [String] :namespace Namespace of the metric
        @option options [Integer] :timestamp Timestamp of the metric
        """

        options_ = Map(
            DeepDict.deep_merge(
                {'tags': self.global_tags,
                 'namespace': self._settings.namespace},
                self._defaults['counter'],
                options or {}
                )
            )

        self.put(
            'counter.%s' % (name,),
            value or 0,
            options_.tags,
            options_.agg,
            options_.agg_freq,
            self._settings.sample_rate,
            options_.namespace,
            options_.timestamp
            )

    def gauge(self, name, value, options=None):
        """
        Adds a Gauge

        Keyword arguments:
        @param name [String] Name of the gauge
        @param value [Numeric] Value of the metric
        @param [Hash] options The options to apply to the metric
        @option options [Hash] :tags Tags to associate to the metric
        @option options [Array<String>] :agg List of aggregations to be
            applied by the Telemetron
        @option options [Integer] :agg_freq Aggregation frequency in seconds
        @option options [String] :namespace Namespace of the metric
        @option options [Integer] :timestamp Timestamp of the metric
        """

        options_ = Map(
            DeepDict.deep_merge(
                {'tags': self.global_tags,
                 'namespace': self._settings.namespace},
                self._defaults['gauge'],
                options or {}
                )
            )

        self.put(
            'gauge.%s' % (name,),
            value or 0,
            options_.tags,
            options_.agg,
            options_.agg_freq,
            self._settings.sample_rate,
            options_.namespace,
            options_.timestamp
            )

    def put(self, name, value, tags=None, agg=None, agg_freq=10,
            sample_rate=100, namespace=None, timestamp=None):
        """
        Adds a new metric to the in-memory buffer.

        Keyword arguments:
        @param name [String] Name of the gauge
        @param value [Numeric] Value of the metric
        @param tags [Hash] Tags to associate to the metric
        @param agg [Array<String>] List of aggregations to be applied by the
            Telemetron
        @param sample_rate [Integer] Sample rate to apply
        @param agg_freq [Array<Integer>] Aggregation frequency in seconds
        @param namespace [String] Namespace of the metric
        @param timestamp [Integer] Timestamp of the metric
        """
        options = (
            ('tags', tags),
            ('agg', agg),
            ('agg_freq', agg_freq),
            ('namespace', namespace),
            ('timestamp', timestamp or int(time.time()))
        )

        options = dict(((key, val) for key, val in options
                        if val is not None))

        opt = Map(
            DeepDict.deep_merge(
                {'tags': self.global_tags,
                 'namespace': self._settings.namespace},
                self._defaults['_put'],
                options
                )
            )

        opt.timestamp = opt.timestamp or int(time.time())
        opt.sample_rate = sample_rate

        if sample_rate is not None and (sample_rate < 1 or sample_rate > 100):
            raise TelemetronValueError("Sample rate out of range")

        sample_rate_normalized = (sample_rate or 100.0) / 100.0

        if random.random() <= sample_rate_normalized:
            line = make_line(self._settings.prefix, name, value, **opt)
            self.put_raw(line)

    def put_raw(self, lines):
        """
        Insert a raw line into the buffer (use with caution)

        Keyword arguments:
        lines -- if lines is a list, insert every element into the buffer.
        If it's a single line, insert it into the buffer.
        """

        if not self.transport_initialized():
            raise TransportNotInitialized

        self.log.debug(
            "Appending to buffer %s  (%d)",
            lines,
            len(self._buffer)
            )

        if isinstance(lines, list):
            for line in lines:
                self._buffer.append(line)
                if self.buffer_count >= self._settings.flush_size:
                    self.flush()
        else:
            self._buffer.append(lines)
            if self.buffer_count >= self._settings.flush_size:
                self.flush()

    def flush(self):
        """
        Flush buffer to socket

        Keyword arguments:
        send_buffer_length -- if True, appends a metric to the buffer with
            the current buffer length

        Raises TransportNotInitialized is init_transport() wasn't called.
        """

        if not self.transport_initialized():
            raise TransportNotInitialized

        sent_with_success = False
        if len(self._buffer) > 0:
            # HACK: the following is a basic protection against flush failure
            if self.system_stats and \
                    self.buffer_count <= self._settings.flush_size:
                self.put(
                    name="buffer.flush_length",
                    tags={},
                    value=len(self._buffer),
                    agg=['avg']
                    )

            message = "%s\n" % ("\n".join(self._buffer),)
            self.log.info(
                "About to flush %d lines on a %d byte message",
                len(self._buffer),
                len(message)
                )
            self.log.debug("Whole message to be flushed: %s", message)

            if self._settings.transport.lower() == self.TRANSPORT_TCP:
                error = self._socket.sendall(message)
                sent_with_success = error is None
            elif self._settings.transport.lower() == self.TRANSPORT_UDP:
                sent = self._socket.sendto(
                    message,
                    (self._settings.host, self._settings.port)
                    )
                sent_with_success = len(message) == sent
            elif self._settings.transport.lower() == self.TRANSPORT_API \
                    or self._settings.transport.lower() == \
                    self.TRANSPORT_API_SSL:

                headers = {
                    "User-Agent": api_client_user_agent(),
                    "M-Api-Token": self._settings.api_token,
                    "content-type": "applicaton/text"
                    }

                body = "%s\n" % (message,)

                res = self._pool.request(
                    'PUT',
                    TelemetronClient.API_PATH,
                    headers=headers,
                    timeout=self._settings.timeout,
                    body=body
                    )

                self.log.debug("API headers: %s", headers)
                self.log.info("%s transport return code is %s",
                              self._settings.transport, res.status)

                if res.status == 201:
                    sent_with_success = True

            if not sent_with_success:
                self._flush_fail_count += 1
                self.log.error("Flush failed. Count %d" % (
                    self._flush_fail_count,))
            else:
                self._flush_fail_count = 0
                self._buffer = []

            return sent_with_success

    def __buffer_count(self):
        """
        Returns the current number of messages in buffer.
        """

        return len(self._buffer)

    buffer_count = property(__buffer_count)
