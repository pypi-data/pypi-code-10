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
import json
from xml.dom import minidom
from rdflib.graph import Graph

from .client import RedlinkClient
from .format import from_mimetype, Format


class RedlinkAnalysis(RedlinkClient):
    """
    Redlink Analysis Client
    """

    path = "analysis"
    enhance_path = "enhance"

    def __init__(self, key):
        """
        @type key: str
        @param key: api key
        """
        super(RedlinkAnalysis, self).__init__(key)

    def enhance(self, content, input=Format.TEXT, output=Format.JSON):
        """
        Enhance the content

        @type content: str
        @param content: target content

        @type input: C{FormatDef}
        @param input: input type

        @type output: C{FormatDef}
        @param output: output type

        @return: enhancements
        """
        analysis = self.status["analyses"][0]
        params = {
            self.param_in: input.name,
            self.param_out: output.name
        }
        resource = self._build_url("/%s/%s/%s" % (self.path, analysis, self.enhance_path), params)
        logging.debug("Making request to %s" % resource)

        response = self._post(resource, content, input.mimetype, output.mimetype)

        if response.status_code != 200:
            logging.error("Enhance request returned %d: %s" % (response.status_code, response.reason))
            return response.text
        else:
            content_type = from_mimetype(response.headers["Content-Type"])
            if content_type == Format.JSON or content_type == Format.REDLINKJSON:
                return json.loads(response.text)
            elif content_type == Format.XML or content_type == Format.REDLINKXML:
                return minidom.parse(response.text)
            elif content_type.rdflibMapping:
                g = Graph()
                g.parse(data=response.text, format=content_type.rdflibMapping)
                return g
            else:
                logging.warn("Handler not found for %s, so returning raw text response..." % content_type.mimetype)
                return response.text
