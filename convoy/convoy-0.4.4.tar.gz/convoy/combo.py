#   Convoy is a WSGI app for loading multiple files in the same request.
#   Copyright (C) 2011-2015 Canonical, Ltd.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import logging
import os.path
import re
import sys

try:
    from urllib.parse import parse_qsl
except ImportError:
    from cgi import parse_qsl

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse


CHUNK_SIZE = 2 << 12
URL_RE = re.compile(b"""url[(][ "']*([^ "')]+)[ "']*[)]""")
URL_PARSE = re.compile(b"/([^/]*).*?$")


def relative_path(from_file, to_file):
    """Return the relative path between from_file and to_file."""
    dir_from, base_from = os.path.split(from_file)
    dir_to, base_to = os.path.split(to_file)
    path = os.path.relpath(dir_to, dir_from)
    if path == ".":
        return base_to
    return os.path.join(path, base_to)


def parse_url(url):
    """Parse a combo URL.

    Returns the list of arguments in the original order.
    """
    scheme, loc, path, query, frag = urlparse.urlsplit(url)
    return parse_qs(query)


def parse_qs(query):
    """Parse a query string.

    Returns the list of arguments in the original order.
    """
    params = parse_qsl(query, keep_blank_values=True)
    return tuple([param for param, value in params])


class InvalidFileError(Exception):
    """Exception raised for bogus filenames."""


def validate_files(fnames, root):
    """Validate that the given filenames are sane.

    Filenames must be within the root directory and actual files.

    @raises InvalidFileError for any bogus files.
    """
    for fname in fnames:
        full = os.path.abspath(os.path.join(root, fname))
        if not (full.startswith(root) and os.path.isfile(full)):
            raise InvalidFileError(fname)


def combine_files(fnames, root, resource_prefix="", rewrite_urls=True):
    """Combine many files into one.

    Returns an iterator with the combined content of all the
    files. The relative path to root will be included as a comment
    between each file.
    """
    # Used when encoding local file-system paths.
    fsenc = sys.getfilesystemencoding()

    if not isinstance(root, bytes):
        # This is a local file-system path.
        root = root.encode(fsenc)
    if not isinstance(resource_prefix, bytes):
        # This is a URL component, so assume only ASCII is okay.
        resource_prefix = resource_prefix.encode("ascii")

    resource_prefix = resource_prefix.rstrip(b"/")

    for fname in fnames:
        if not isinstance(fname, bytes):
            # This is a local file-system path.
            fname = fname.encode(fsenc)

        file_ext = os.path.splitext(fname)[-1]
        basename = os.path.basename(fname)
        full = os.path.abspath(os.path.join(root, fname))
        if (full.startswith(root) and os.path.isfile(full)):
            yield b"/* " + fname + b" */\n"
            with open(full, "rb") as f:
                if file_ext == b".css" and rewrite_urls:
                    file_content = f.read()
                    src_dir = os.path.dirname(full)
                    relative_parts = relative_path(
                        os.path.join(root, basename), src_dir).split(
                        os.path.sep.encode(fsenc))

                    def fix_relative_url(match):
                        url = match.group(1)
                        # Don't modify absolute URLs or 'data:' urls.
                        if (url.startswith(b"http") or
                                url.startswith(b"/") or
                                url.startswith(b"data:")):
                            return match.group(0)
                        parts = relative_parts + url.split(b"/")
                        result = []
                        for part in parts:
                            if part == b".." and result[-1:] != [b".."]:
                                result.pop(-1)
                                continue
                            result.append(part)
                        return b"url(x)".replace(b"x", b"/".join(
                            part for part in [resource_prefix] + result
                            if part))

                    file_content = URL_RE.sub(fix_relative_url, file_content)
                    yield file_content
                    yield b"\n"
                else:
                    while True:
                        chunk = f.read(CHUNK_SIZE)
                        if not chunk:
                            yield b"\n"
                            break
                        yield chunk


def combo_app(
        root, resource_prefix="", rewrite_urls=True, additional_headers=None):
    """A simple YUI Combo Service WSGI app.

    Serves any files under C{root}, setting an appropriate
    C{Content-Type} header.
    Additional headers can be provided as a list of tuples to allow
    for generic extensions, but their correctness won't be verified.
    """
    root = os.path.abspath(root)
    log = logging.getLogger(__name__)

    def app(environ, start_response, root=root):
        # Path hint uses the rest of the url to map to files on disk based off
        # the root specified to convoy.
        path_hint = environ['PATH_INFO'].strip('/')
        fnames = parse_qs(environ["QUERY_STRING"])
        content_type = "text/plain"
        if fnames:
            if fnames[0].endswith(".js"):
                content_type = "text/javascript"
            elif fnames[0].endswith(".css"):
                content_type = "text/css"
        else:
            log.info('No files in querystring.')
            start_response("404 Not Found", [("Content-Type", content_type)])
            return (b"Not Found",)

        # Take any prefix in the url route into consideration for the root to
        # find files.
        updated_root = os.path.join(root, path_hint)
        # Enforce that the updated root is not outside the original root.
        absroot = os.path.abspath(updated_root)
        if not absroot.startswith(os.path.abspath(root)):
            log.info('Updated root is outside of original root.')
            start_response("400 Bad Request", [("Content-Type", content_type)])
            return (b"Bad Request",)
        headers = [("Content-Type", content_type),
                   ("X-Content-Type-Options", "nosniff")]
        if additional_headers is not None:
            headers.extend(additional_headers)
        try:
            validate_files(fnames, updated_root)
        except InvalidFileError as if_error:
            log.info('No such file: %s' % if_error.args[0])
            start_response("400 Bad Request", headers)
            return (b"Bad Request",)
        else:
            start_response("200 OK", headers)
            return combine_files(fnames, updated_root, resource_prefix,
                                 rewrite_urls=rewrite_urls)
    return app
