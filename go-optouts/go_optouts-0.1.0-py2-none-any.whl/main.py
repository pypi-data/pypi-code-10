""" Command for launching the Vumi Go Opt Out API. """

import click

from .server import ApiSite


@click.command("go-optouts")
@click.version_option()
@click.option(
    '--config', '-c',
    required=True,
    help='YAML config file')
@click.option(
    '--host', '-h',
    default='localhost',
    help='Host to listen on')
@click.option(
    '--port', '-p',
    type=int, default=8080,
    help='Port to listen on')
def run(config, host, port):
    """ Vumi Go Opt Out API. """
    site = ApiSite(config)
    site.run(host, port)
