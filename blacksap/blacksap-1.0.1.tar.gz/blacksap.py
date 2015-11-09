#!/usr/bin/env python
# coding=utf-8
"""Watch Torrent RSS feeds and download new torrent files.
"""
from __future__ import print_function
import os
import sys
import click
import json
import hashlib
import requests
import feedparser
import time
from commands import getstatusoutput

__author__ = 'Jesse Almanrode (jesse@almanrode.com)'
debug = False
cfg_file = '~/.blacksap.cfg'


def read_cfg():
    """Load the config file

    :return: Dictionary
    """
    global debug, cfg_file
    if os.path.exists(os.path.expanduser(cfg_file)):
        f = open(os.path.expanduser(cfg_file))
        cfg = json.load(f)
        f.close()
        return cfg
    else:
        return {'feeds': []}


def write_cfg(cfg):
    """Write config dictionary to config file

    :param cfg: Dictionary of items to write
    :return: True or Exception
    """
    global debug, cfg_file
    f = open(os.path.expanduser(cfg_file), 'wb')
    json.dump(cfg, f, indent=4)
    f.close()
    return True


def ttl_expired(timestamp, ttl):
    """Is the current cache expired

    :param timestamp: Last time the feed was checked.
    :param ttl: Amount of time for cache to be considered valid (in seconds)
    """
    global debug
    if timestamp is None:
        return True
    now = int(time.time())
    if now - timestamp > ttl:
        return True
    else:
        return False


def download_torrent_file(url, destination, filename, maxtries):
    """Attempt to download a torrent file to a destination

    :param url: URL of torrent file
    :param destination: POSX path to output location
    :param filename: Name of the output file
    :param maxtries: Number of times to try to download file
    :return: True or False
    """
    # TODO - Get this using requests module rather than curl
    global debug
    if '?' in url:
        short_url = str(url.split('?')[0])
    else:
        short_url = url
    for x in xrange(0, maxtries):
        if debug:
            click.echo('Attempting: curl --compressed -G -q "' + short_url + '" -o "' + destination + filename + '"')
        result = getstatusoutput('curl --compressed -G -q "' + short_url + '" -o "' + destination + filename + '"')
        if result[0] != 0 and x > maxtries:
            if debug:
                click.secho('Unable to download: ' + url, fg='red')
            return False
        elif result[0] == 0:
            if debug:
                click.echo('Downloaded: ' + short_url + ' in ' + str(x) + ' tries')
            return True
    click.secho('Download attempts exceeded for torrent: ' + url, fg='red')
    return False


@click.group()
@click.option('--verbose', is_flag=True, help='Enable debuging')
@click.version_option()
def cli(verbose):
    """Manage RSS Torrent feeds to feed Transmission
    """
    global debug
    debug = verbose


@cli.command()
@click.argument('urls', nargs=-1)
def clearcache(urls):
    """Clear the hash, last, and ttl fields from one or all feeds
    """
    global debug
    cfg = read_cfg()
    if len(cfg['feeds']) == 0:
        click.secho('No feeds being tracked', fg='red')
        sys.exit(1)
    else:
        for feed in cfg['feeds']:
            if len(urls) > 0:
                if feed['url'] in urls:
                    feed['hash'] = None
                    feed['last'] = None
                    feed['ttl'] = None
                    click.secho('Cache cleared for: ' + feed['url'], fg='green')
            else:
                feed['hash'] = None
                feed['last'] = None
                feed['ttl'] = None
        write_cfg(cfg)
        if len(urls) < 1:
            click.secho('All caches cleared', fg='green')


@cli.command()
@click.argument('urls', nargs=-1, required=True)
def track(urls):
    """Add RSS feed(s) to tracking
    """
    global debug
    cfg = read_cfg()
    for url in urls:
        if debug:
            click.echo('Attempting to download/verify RSS feed from: ' + url)
        try:
            rss_feed_raw = requests.get(url, timeout=5)
            rss_feed_raw = rss_feed_raw.text
        except requests.exceptions.Timeout:
            click.secho('Unable to download: ' + url, fg='red')
            continue
        if debug:
            click.echo('RSS feed downloaded successfully')
        rss_feed = feedparser.parse(rss_feed_raw)
        feed = dict()
        feed['name'] = rss_feed['feed']['title']
        feed['url'] = url
        feed['hash'] = None
        feed['last'] = None
        feed['ttl'] = None
        feed['new'] = True
        if feed not in cfg['feeds']:
            cfg['feeds'].append(feed)
            write_cfg(cfg)
            click.secho('Added RSS feed: ' + feed['name'], fg='green')
        else:
            click.secho('RSS feed already exists!', fg='red')
            sys.exit(0)


@cli.command()
@click.argument('urls', nargs=-1, required=True)
def untrack(urls):
    """Stop tracking RSS feed(s)
    """
    global debug
    cfg = read_cfg()
    for url in urls:
        feeds = [x for x in cfg['feeds'] if x['url'] != url]
        if len(feeds) == 0:
            click.secho('URL is not being tracked: ' + url, fg='red')
        cfg['feeds'] = feeds
    write_cfg(cfg)
    click.echo('Removed feed(s) from config')


@cli.command()
def tracking():
    """List tracked RSS feeds
    """
    global debug
    cfg = read_cfg()
    if len(cfg['feeds']) == 0:
        click.secho('Zero feeds tracked', fg='green')
        sys.exit(0)
    else:
        click.secho(str(len(cfg['feeds'])) + ' feeds tracked', fg='green')
        for feed in cfg['feeds']:
            click.echo('-' * 20)
            click.echo('Name: ' + feed['name'])
            click.echo('URL: ' + feed['url'])


@cli.command()
@click.option('--count', default=-1, help='Number of torrent files to download (default = -1)')
@click.option('--force', is_flag=True, help='Force a new download of the RSS feed')
@click.option('--new', is_flag=True, help='Force a new feed to download items rather than cache most recent')
@click.option('--maxretries', default=5, help='Number of times to try and download .torrent file (default = 5)')
@click.option('--ttl', default=600, help='TTL for cache in seconds (default = 600)')
@click.option('--reverse', is_flag=True, help='Read the feeds in reverse order (oldest to newest)')
@click.argument('outputdir', type=click.Path())
def run(count, force, new, maxretries, ttl, reverse, outputdir):
    """Check all tracked feeds for new content and download torrent files as needed
    """
    # TODO - Allow individual feeds to be updated by url
    global debug
    cfg = read_cfg()
    if outputdir.endswith('/') is False:
        outputdir += '/'
    outputdir = os.path.expanduser(outputdir)
    if os.path.exists(outputdir) is False:
        click.secho('Please create path: ' + outputdir, fg='red')
        sys.exit(1)
    if len(cfg['feeds']) == 0:
        click.secho('Zero feeds being tracked', fg='red')
        sys.exit(1)
    else:
        starttime = time.time()
        for feed in cfg['feeds']:
            if ttl_expired(feed['ttl'], ttl) is False and force is False:
                click.secho('TTL for: ' + feed['url'] + ' has not expired yet.  Use --force to bypass',
                            fg='yellow')
                continue
            if debug:
                click.echo('Downloading feed: ' + feed['url'])
            try:
                rss_feed_raw = requests.get(feed['url'], timeout=5)
                rss_feed_raw = rss_feed_raw.text
            except requests.exceptions.Timeout:
                click.secho('Unable to download: ' + feed['url'], fg='red')
                continue
            feed['ttl'] = int(time.time())  # Update the timestamp for the ttl
            feed_md5 = hashlib.md5(rss_feed_raw.encode('utf-8')).hexdigest()
            if feed['hash'] == feed_md5 and force is False:
                if debug:
                    click.echo('Feed has not changed: ' + feed['url'])
                write_cfg(cfg)
            else:
                rss_feed = feedparser.parse(rss_feed_raw)
                rss_entries = rss_feed['entries']
                if debug:
                    click.echo('Feed contains ' + str(len(rss_entries)) + ' entries')
                counter = 0
                # This is so we can keep track of what the "most recent torrent" downloaded was
                downloaded_torrents = list()
                if reverse:
                    rss_entries = reversed(rss_entries)
                for torrent in rss_entries:
                    torrent_name = torrent['torrent_filename']
                    if feed['new']:
                        downloaded_torrents.append(torrent_name)
                        feed['new'] = False
                        if new is False:
                            break
                    if count <= 0 and torrent_name == feed['last']:
                        if debug:
                            click.echo('No new items in: ' + feed['url'])
                        break
                    torrent_url = [x['href'] for x in torrent['links'] if x['type'] == 'application/x-bittorrent']
                    download_torrent_file(torrent_url.pop(), outputdir, torrent_name, maxretries)
                    downloaded_torrents.append(torrent_name)
                    if count >= 0:
                        counter += 1
                        if counter >= count:
                            break
                # Update the md5 hash for the feed cache
                feed['hash'] = feed_md5
                if len(downloaded_torrents) > 0:
                    click.echo('Downloaded ' + str(len(downloaded_torrents)) + ' new torrents')
                    # Cache the most recent torrent downloaded
                    if reverse:
                        feed['last'] = downloaded_torrents.pop()
                    else:
                        feed['last'] = downloaded_torrents[0]
                write_cfg(cfg)
        endtime = time.time()
        deltatime = endtime - starttime
        deltatime = format(float(deltatime), '.4f')
        click.secho(str(len(cfg['feeds'])) + " RSS feeds checked in: " + deltatime + ' seconds', fg='green')


if __name__ == '__main__':
    cli()
