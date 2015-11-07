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


class FormatDef:
    """
    Format (internal) definition
    """

    def __init__(self, name, mimetype, rdflibMapping=None):
        self.name = name
        self.mimetype = mimetype
        self.rdflibMapping = rdflibMapping

    def __str__(self):
        return "%s[%s]" % (self.name, self.mimetype)

    def __cmp__(self, other):
        if other is None:
            return -1
        elif isinstance(other, FormatDef):
            return -1 * int(not self.mimetype == other.mimetype)
        elif "/" in other:
            if ";" in other:
                return -1 * int(not self.mimetype == other.split(";")[0])
            else:
                return -1 * int(not self.mimetype == other)
        else:
            return -1 * int(not self.name == other)

    def __eq__(self, other):
        if other is None:
            return -1
        elif isinstance(other, FormatDef):
            return self.mimetype == other.mimetype
        elif "/" in other:
            if ";" in other:
                return self.mimetype == other.split(";")[0]
            else:
                return self.mimetype == other
        else:
            return self.name == other


class Format:
    """
    Redlink formats
    """

    TEXT = FormatDef("text", "text/plain")
    PDF = FormatDef("pdf", "application/pdf")
    HTML = FormatDef("html", "text/html")
    OFFICE = FormatDef("office", "application/doc")
    OCTETSTREAM = FormatDef("octetstream", "application/octet-stream")

    JSON = FormatDef("json", "application/json")
    XML = FormatDef("xml", "application/xml")
    REDLINKJSON = FormatDef("redlinkjson", "application/redlink-analysis+json")
    REDLINKXML = FormatDef("redlinkxml", "application/redlink-analysis+xml")

    JSONLD = FormatDef("jsonld", "application/ld+json", "json-ld")
    RDFXML = FormatDef("rdfxml", "application/rdf+xml", "xml")
    RDFJSON = FormatDef("rdfjson", "application/rdf+json")
    TURTLE = FormatDef("turtle", "text/turtle", "turtle")
    NT = FormatDef("nt", "text/rdf+n3", "n3")


def from_mimetype(mimetype):
    """
    Returns a C{FormatDef} representing the passed mimetype

    @type mimetype: str
    @param mimetype: format mimetype
    @return: format
    """
    for name, format in Format.__dict__.items():
        if isinstance(format, FormatDef):
            if format == mimetype:
                return format
    return None
