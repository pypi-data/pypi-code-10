# -*- coding: utf8 -*-

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from rdflib.graph import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, POST, POSTDIRECTLY
import json

from . import __agent__
from .client import RedlinkClient
from .format import from_mimetype, Format


class RedlinkData(RedlinkClient):
    """
    Redlink Data Client
    """

    path = "data"
    release_path = "release"
    resource_path = "resource"
    param_uri = "uri"
    sparql_path = "sparql"
    sparql_select_path = "select"
    sparql_update_path = "update"
    ldpath_path = "ldpath"

    def __init__(self, key):
        """
        @type key: str
        @param key: api key
        """
        super(RedlinkData, self).__init__(key)

    def release(self, dataset):
        """
        Release the data in the dataset to be used for analysis

        @param dataset: dataset name
        """
        resource = self._build_url("/%s/%s/%s" % (self.path, dataset, self.release_path))
        response = self._post(resource, accept="application/json")
        return 200 <= response.status_code < 300

    def import_dataset(self, data, mimetype, dataset, clean_before=False):
        """
        Import RDF data into the dataset

        @param data: data to import, either as C{str}, {rdflib.Graph} or C{file}
        @param mimetype: mimetype of the data
        @param dataset: dataset name
        @param clean_before: clean data in dataset before importing (default=False)

        @rtype: C{bool}
        @return: success or not
        """
        resource = self._build_url("/%s/%s" % (self.path, dataset))

        rdf_format = from_mimetype(mimetype)
        if not rdf_format:
            rdf_format = Format.TURTLE

        payload = self._get_payload_from_data(data, rdf_format)
        method = self._put if clean_before else self._post
        response = method(resource, payload, contentType=rdf_format.mimetype)
        return 200 <= response.status_code < 300

    def export_dataset(self, dataset):
        """
        Export the RDF data from a dataset

        @param dataset: dataset name

        @rtype: C{rdflib.Graph}
        @return: data
        """
        resource = self._build_url("/%s/%s" % (self.path, dataset))
        rdf_format = Format.TURTLE
        response = self._get(resource, accept=rdf_format.mimetype)
        contentType = from_mimetype(response.headers["Content-Type"])
        if contentType.rdflibMapping:
            g = Graph()
            g.parse(data=response.text, format=contentType.rdflibMapping)
            return g
        else:
            logging.warn("Handler not found for parsing %s as RDF, so returning raw response..." % contentType.mimetype)
            return response.text

    def clean_dataset(self, dataset):
        """
        Clean a data in a dataset

        @param dataset: dataset name

        @rtype: C{bool}
        @return: success or not
        """
        resource = self._build_url("/%s/%s" % (self.path, dataset))
        response = self._delete(resource)
        return 200 <= response.status_code < 300

    def import_resource(self, data, mimetype, uri, dataset, clean_before=False):
        """
        Import data for a resource

        @param data: data to import, either as C{str}, {rdflib.Graph} or C{file}
        @param mimetype: mimetype of the data
        @param uri: reource uri
        @param dataset: dataset name
        @param clean_before: clean data in dataset before importing (default=False)

        @rtype: C{bool}
        @return: success or not
        """
        resource = self._build_url("/%s/%s/%s" % (self.path, dataset, self.resource_path), {self.param_uri: uri})

        rdf_format = from_mimetype(mimetype)
        if not rdf_format:
            rdf_format = Format.TURTLE

        payload = self._get_payload_from_data(data, rdf_format)
        method = self._put if clean_before else self._post
        response = method(resource, payload, contentType=rdf_format.mimetype)
        return 200 <= response.status_code < 300

    def export_resource(self, uri, dataset):
        """
        Export the RDF data from a resource

        @param uri: resource uri
        @param dataset: dataset name

        @rtype: C{rdflib.Graph}
        @return: data
        """
        resource = self._build_url("/%s/%s/%s" % (self.path, dataset, self.resource_path), {self.param_uri: uri})
        rdf_format = Format.TURTLE
        response = self._get(resource, accept=rdf_format.mimetype)
        contentType = from_mimetype(response.headers["Content-Type"])
        if contentType.rdflibMapping:
            g = Graph()
            g.parse(data=response.text, format=contentType.rdflibMapping)
            return g
        else:
            logging.warn("Handler not found for parsing %s as RDF, so returning raw response..." % contentType.mimetype)
            return response.text

    def delete_resource(self, uri, dataset):
        """
        Delete a resource

        @param uri: resource uri
        @param dataset: dataset name

        @rtype: C{bool}
        @return: success or not
        """
        resource = self._build_url("/%s/%s/%s" % (self.path, dataset, self.resource_path), {self.param_uri: uri})
        response = self._delete(resource)
        return 200 <= response.status_code < 300

    def sparql_tuple_query(self, query, dataset):
        """
        Execute a tuple query (SELECT or ASK)

        @param query: query
        @param dataset: dataset name
        @rtype: C{dict}
        @return: query results
        """
        return self._sparql_query(dataset, query, Format.JSON.name)

    def sparql_graph_query(self, query, dataset):
        """
        Execute a graph query (CONSTRUCT or DESCRIBE)

        @param query: query
        @param dataset: dataset name
        @rtype: C{rdflib.Graph}
        @return: query results
        """
        return self._sparql_query(dataset, query, Format.TURTLE.name)

    def sparql_update(self, query, dataset):
        """
        Execute an update query

        @param query: query
        @param dataset: dataset name
        @return: query results
        """
        return self._sparql_query(dataset, query, Format.JSON.name)

    def _sparql_query(self, dataset, query, format=JSON):
        sparql_endpoint_select = "%s/%s/%s/%s/%s/%s" % (self.endpoint, self.version, self.path,
                                                        dataset, self.sparql_path, self.sparql_select_path)
        sparql_endpoint_update = "%s/%s/%s/%s/%s/%s" % (self.endpoint, self.version, self.path,
                                                        dataset, self.sparql_path, self.sparql_update_path)
        sparql = SPARQLWrapper(sparql_endpoint_select, sparql_endpoint_update)
        sparql.addCustomParameter(self.param_key, self.key)
        sparql.agent = __agent__
        sparql.setMethod(POST)
        sparql.setRequestMethod(POSTDIRECTLY)
        sparql.setReturnFormat(format)
        sparql.setQuery(query)
        return sparql.query().convert()

    def _get_payload_from_data(self, data, rdf_format):
        # TODO: do this in a more pythonic way
        if (data):
            if isinstance(data, str):
                return data
            elif isinstance(data, Graph):
                return data.serialize(format=rdf_format.rdflibMapping)
            elif hasattr(data, 'read'):
                raw = data.read()
                try:
                    return raw.encode('UTF-8')
                except UnicodeDecodeError:
                    return raw
            else:
                raise ValueError("unsupported type %s as data payload" % type(data))
        else:
            return None

    def _build_dataset_base_uri(self, dataset):
        return "%s/%s/%s/" % (self.datahub, self.status["owner"], dataset)

    def ldpath(self, uri, program, dataset):
        """
        Ezecute a LDPath program

        @param uri: context resource uri
        @param program: ldpath program
        @param dataset: dataset name
        @rtype: C{dict}
        @return: results
        """
        resource = self._build_url("/%s/%s/%s" % (self.path, dataset, self.ldpath_path), {self.param_uri: uri})
        response = self._post(resource, program, accept=Format.JSON.mimetype)
        if 200 <= response.status_code < 300:
            contentType = from_mimetype(response.headers["Content-Type"])
            if Format.JSON == contentType:
                return json.loads(response.text)
            else:
                logging.warn("Content type should be 'application/json' but was %s" % response.headers["Content-Type"])
                return response.text
        else:
            raise RuntimeError("LDPath program evaluation returned %d: %s", response.status_code, response.reason)
