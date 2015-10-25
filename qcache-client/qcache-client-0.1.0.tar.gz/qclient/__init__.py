from contextlib import contextmanager
import json
import requests
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout, RequestException
from qclient.node_ring import NodeRing
from collections import defaultdict


__version__ = "0.1.0"


class QClientException(Exception):
    pass


class NoCacheAvailable(QClientException):
    pass


class UnexpectedServerResponse(QClientException):
    pass


class MalformedQueryException(QClientException):
    pass


class UnsupportedAcceptType(QClientException):
    pass


def _node_statisticts():
    return dict(connect_timeout=0,
                connection_error=0,
                read_timeout=0,
                unknown_error=0,
                resurrections=0,
                retry_error=0)


class QClient(object):
    def __init__(self, node_list, connect_timeout=1.0, read_timeout=2.0):
        self.node_ring = NodeRing(node_list)
        self.failing_nodes = set()
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.statistics = defaultdict(_node_statisticts)
        self.check_interval = 10
        self.post_count = 0

    def _node_for_key(self, key):
        node = self.node_ring.get_node(key)
        if not node:
            # Check all caches in unreachable nodes, if none exist. Fail!
            self._test_dropped_nodes()
            node = self.node_ring.get_node(key)
            if not node:
                raise NoCacheAvailable('No QCaches reachable')

        return node

    def _test_dropped_nodes(self):
        # Test all nodes that are currently on the fail list. Any node that responds
        # gets reinserted into the node ring. A more selective strategy may be required
        # in the future but keep it simple for now.
        for node in list(self.failing_nodes):
            status_url = self._status_url(node)
            try:
                response = requests.get(status_url)
                if response.status_code == 200:
                    self.node_ring.add_node(node)
                    self.failing_nodes.remove(node)
                    self.statistics[node]['resurrections'] += 1
            except RequestException:
                self.statistics[node]['retry_error'] += 1

    def _drop_node(self, node):
        self.node_ring.remove_node(node)
        self.failing_nodes.add(node)

    def _check_dropped_nodes(self):
        if self.post_count % self.check_interval == 0:
            self._test_dropped_nodes()

        self.post_count += 1

    @contextmanager
    def connection_error_manager(self, node):
        try:
            yield
        except ConnectTimeout:
            self.statistics[node]['connect_timeout'] += 1
            self._drop_node(node)
        except ConnectionError:
            self.statistics[node]['connection_error'] += 1
            self._drop_node(node)
        except ReadTimeout:
            self.statistics[node]['read_timeout'] += 1
            self._drop_node(node)

    @staticmethod
    def _status_url(node):
        new_node = node if node.endswith('/') else node + '/'
        return new_node + 'qcache/status'

    @staticmethod
    def _key_url(node, key):
        new_node = node if node.endswith('/') else node + '/'
        return new_node + 'qcache/dataset/' + key

    def get(self, key, q, accept='application/json'):
        json_q = json.dumps(q)

        while True:
            node = self._node_for_key(key)
            key_url = self._key_url(node, key)
            with self.connection_error_manager(node):
                response = requests.get(key_url, params={'q': json_q}, headers={'Accept': accept},
                                        timeout=(self.connect_timeout, self.read_timeout))
                if response.status_code == 200:
                    return response.content

                if response.status_code == 404:
                    return None

                if response.status_code == 400:
                    raise MalformedQueryException('Malformed query "{json_q}", server response "{server_response}"'.format(
                        json_q=json_q, server_response=response.content))
                elif response.status_code == 406:
                    raise UnsupportedAcceptType('Accept type "{accept}" is not supported'.format(accept))
                else:
                    raise UnexpectedServerResponse('Unable to query dataset, status code {status_code}'.format(
                        status_code=response.status_code))

    def post(self, key, content, content_type='text/csv'):
        # Checking of nodes that have previously been dropped is only done when inserting
        # new data right now. Rationale: If we have successful gets then there is no reason
        # to redistribute any data.
        self._check_dropped_nodes()

        while True:
            node = self._node_for_key(key)
            key_url = self._key_url(node, key)

            with self.connection_error_manager(node):
                response = requests.post(key_url, headers={'Content-type': content_type}, data=content,
                                         timeout=(self.connect_timeout, self.read_timeout))
                if response.status_code == 201:
                    return

                self.statistics[node]['unknown_error'] += 1
                raise UnexpectedServerResponse('Unable to create dataset, status code {status_code}'.format(
                    status_code=response.status_code))

    def query(self, key, q, load_fn, load_fn_kwargs=None, content_type='text/csv', accept='application/json'):
        content = None
        while True:
            result = self.get(key, q, accept)
            if result is not None:
                return result

            if content is None:
                content = load_fn(**load_fn_kwargs)

            self.post(key, content, content_type=content_type)

    def delete(self, key):
        while True:
            node = self._node_for_key(key)
            key_url = self._key_url(node, key)
            with self.connection_error_manager(node):
                requests.delete(key_url, timeout=(self.connect_timeout, self.read_timeout))
                return
