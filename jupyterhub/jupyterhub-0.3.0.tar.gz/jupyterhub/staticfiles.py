"""Standalone static-file server for IPython static files"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import sys

from tornado import options, web, ioloop
from tornado.log import app_log

from IPython.html import DEFAULT_STATIC_FILES_PATH
from IPython.html.utils import url_path_join
from IPython.html.base.handlers import FileFindHandler


def main(opts):
    if opts.path:
        static_path = opts.path.split(':')
    else:
        static_path = [DEFAULT_STATIC_FILES_PATH]
    settings = dict(
        static_handler_class=FileFindHandler,
        static_url_prefix=url_path_join(opts.base_url, 'static/'),
        static_path=static_path,
    )
    app_log.info("Serving files in {path} at {ip}:{port}{url}".format(
        path=':'.join(static_path),
        ip=opts.ip,
        port=opts.port,
        url=settings['static_url_prefix'],
    ))
    
    app = web.Application(**settings)
    app.listen(opts.port, opts.ip)
    
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        app_log.critical("Interrupted")


if __name__ == '__main__':
    options.define('base_url', default='/', help="URL prefix", type=str)
    options.define('port', default=8010, help="run on the given port", type=int)
    options.define('ip', default='localhost', help="Listen on the given IP", type=str)
    options.define('path', default='', help="Serve the given :-separated paths", type=str)
    options.parse_command_line()
    main(options.options)


