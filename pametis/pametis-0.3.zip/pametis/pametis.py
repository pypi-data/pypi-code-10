#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    pametis version 0.3 - Sitemap Analyzer/Parser/Iterator
#    Copyright (c) 2015 Avner Herskovits
#
#    MIT License
#
#    Permission  is  hereby granted, free of charge, to any person  obtaining  a
#    copy of this  software and associated documentation files (the "Software"),
#    to deal in the Software  without  restriction, including without limitation
#    the rights to use, copy, modify, merge,  publish,  distribute,  sublicense,
#    and/or  sell  copies of  the  Software,  and to permit persons to whom  the
#    Software is furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this  permission notice shall be included in
#    all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE  WARRANTIES  OF  MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER
#    LIABILITY, WHETHER IN AN  ACTION  OF  CONTRACT,  TORT OR OTHERWISE, ARISING
#    FROM,  OUT  OF  OR  IN  CONNECTION WITH THE SOFTWARE OR THE  USE  OR  OTHER
#    DEALINGS IN THE SOFTWARE.
#

#
# Imports - stdlib
#
from gzip import decompress
from re import sub
from urllib. request import urlopen
from xml. etree. ElementTree import fromstring

#
# Helper class & function to hold results
#
class _Res( str, object ): pass
def _res( url ):
    res = _Res( url. find( 'loc' ). text )
    res. lastmod, res. changefreq, res. priority = None, None, None
    for i in url:
        if i. tag in ( 'lastmod', 'changefreq', 'priority' ):
            setattr( res, i. tag, i. text )
    return res

#
# Use:
#
# from pametis import sitemap
# for url in sitemap( 'http://example.com/sitemap.xml' ):
#     ... do something with url ...
#
# This function will yield all sitemap leafs, recursing into nested sitemaps
# and decompressing gziped sitemaps.
#
def sitemap( url ):
    with urlopen( url ) as map:
        xmlstr = map. read()
    if url. endswith( '.gz' ):
        xmlstr = decompress( xmlstr ). decode( 'utf-8' )
    else:
        xmlstr = xmlstr. decode( 'utf-8' )
    xmlstr = sub( '<(urlset|sitemapindex)[^>]*>', '<\\1>', xmlstr, count = 1 )  # Get rid of namespaces
    xml = fromstring( xmlstr )
    xmlstr = None
    for child in xml:
        if 'sitemap' == child. tag:
            for loc in child. iter( 'loc' ):
                yield from sitemap( loc. text )
        elif 'url' == child. tag:
            for url in child. iter( 'url' ):
                yield _res( url )

#
# Can be used also as a command line utility, will print to stdout every leaf
# in the sitemap.
#
def _usage():
    print( '''\
pametis OPTIONS|<url>
Prints all the leaf urls in the sitemp.xml pointed to by <url>.

OPTIONS:
-h or --help Show This help message
''' )

def main():
    from sys import argv, stdout
    if 2 != len( argv ):
        _usage()
        exit( 1 )
    elif '-h' == argv[ 1 ] or '--help' == argv[ 1 ]:
        _usage()
        exit( 0 )
    else:
        for i in sitemap( argv[ 1 ]):
            print( i. encode( 'utf-8' ). decode( stdout. encoding ))

if '__main__' == __name__:
    main()
