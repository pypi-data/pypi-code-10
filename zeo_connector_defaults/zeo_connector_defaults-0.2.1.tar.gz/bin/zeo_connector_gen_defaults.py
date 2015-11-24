#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
import os.path
import argparse
from string import Template

dirname = os.path.dirname(__file__)
imported_files = os.path.join(dirname, "../src/")
sys.path.insert(0, os.path.abspath(imported_files))

from zeo_connector_defaults import _SERVER_CONF_PATH
from zeo_connector_defaults import _CLIENT_CONF_PATH


# Functions & classes =========================================================
def create_configuration(args):
    with open(_SERVER_CONF_PATH) as f:
        server_template = f.read()

    with open(_CLIENT_CONF_PATH) as f:
        client_template = f.read()

    if not args.only_server:
        client = Template(client_template).substitute(
            server=args.server,
            port=args.port,
        )
        with open(os.path.basename(_CLIENT_CONF_PATH), "w") as f:
            f.write(client)

    if not args.only_client:
        server = Template(server_template).substitute(
            server=args.server,
            port=args.port,
            path=args.path,
        )
        with open(os.path.basename(_SERVER_CONF_PATH), "w") as f:
            f.write(server)


# Main program ================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""This program will create the default ZEO XML
            configuration files."""
    )
    parser.add_argument(
        "-s",
        "--server",
        default="localhost",
        help="Server url. Default: localhost"
    )
    parser.add_argument(
        "-p",
        "--port",
        default=60985,
        type=int,
        help="Port of the server. Default: 60985"
    )
    parser.add_argument(
        "path",
        metavar="PATH",
        nargs='?',
        default="",
        help="""Path to the database on the server (used in server
            configuration only."""
    )
    parser.add_argument(
        "-C",
        "--only-client",
        action="store_true",
        help="Create only CLIENT configuration."
    )
    parser.add_argument(
        "-S",
        "--only-server",
        action="store_true",
        help="Create only SERVER configuration."
    )

    args = parser.parse_args()

    if not args.only_client and not args.path:
        sys.stderr.write(
            "You have to specify path to the database on for the DB server.\n"
        )
        sys.exit(1)

    if args.only_client and args.only_server:
        sys.stderr.write(
            "You can't have --only-client and --only-server together!\n"
        )
        sys.exit(1)

    create_configuration(args)
