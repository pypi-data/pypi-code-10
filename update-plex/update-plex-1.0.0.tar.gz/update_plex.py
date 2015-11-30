import configparser
import os
import xml.etree.cElementTree as etree

import click
import requests


@click.command()
@click.option('--host')
def run(host):
    if not host:
        config = configparser.ConfigParser()
        config.read(os.path.expanduser('~/.config/update_plex'))
        host = config['DEFAULT']['host']

    url = 'http://{}/library/sections'.format(host)

    s = requests.Session()
    r = s.get(url)
    r.raise_for_status()

    path = './/Directory[@type="show"]'
    for section in etree.fromstring(r.content).findall(path):
        url = '{}/{}/refresh'.format(url, section.attrib['key'])
        r = s.get(url)
        r.raise_for_status()


if __name__ == '__main__':
    run()
