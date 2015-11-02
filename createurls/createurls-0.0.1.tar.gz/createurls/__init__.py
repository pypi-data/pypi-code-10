#!/usr/bin/env python
"""
Requires apachelog.  `pip install apachelog`
"""
import apachelog
import csv
import re
import sys
from optparse import OptionParser

STATUS_CODE = '%&gt;s'
REQUEST = '%r'
USER_AGENT = '%{User-Agent}i'

MEDIA_RE = re.compile(r'\.png|\.jpg|\.jpeg|\.gif|\.tif|\.tiff|\.bmp|\.js|\.css|\.ico|\.swf|\.xml')
SPECIAL_RE = re.compile(r'xd_receiver|\.htj|\.htc|/admin')


def main():
    usage = "usage: %prog [options] LOGFILE"
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-o", "--outfile",
        dest="outfile",
        action="store",
        default="urls.csv",
        help="The output file to write urls to",
        metavar="OUTFILE"
    )
    parser.add_option(
        "-f", "--format",
        dest="logformat",
        action="store",
        default=r'%h %l %u %t \"%r\" %&gt;s %b \"%{Referer}i\" \"%{User-Agent}i\"',
        help="The Apache log format, copied and pasted from the Apache conf",
        metavar="FORMAT"
    )
    parser.add_option(
        "-g", "--grep",
        dest="grep",
        action="store",
        help="Simple, plain text filtering of the log lines. No regexes. This "
             "is useful for things like date filtering - DD/Mmm/YYYY.",
        metavar="TEXT"
    )
    options, args = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    create_urls(args[0], options.outfile, options.logformat, options.grep)


def create_urls(logfile, outfile, logformat, grep=None):
    parser = apachelog.parser(logformat)

    with open(logfile) as f, open(outfile, 'w') as o:
        writer = csv.writer(o)

        # Status spinner
        spinner = "|/-\\"
        pos = 0

        for i, line in enumerate(f):
            # Spin the spinner
            if i % 10000 == 0:
                sys.stdout.write("\r" + spinner[pos])
                sys.stdout.flush()
                pos += 1
                pos %= len(spinner)

            # If a filter was specified, filter by it
            if grep and not grep in line:
                continue

            try:
                data = parser.parse(line)
            except apachelog.ApacheLogParserError as e:
                print(e)
                continue

            if data[STATUS_CODE] != '200':
                continue

            method, url, protocol = data[REQUEST].split()

            # Check for GET requests with a status of 200
            if method != 'GET':
                continue

            # Exclude media requests and special urls
            if MEDIA_RE.search(url) or SPECIAL_RE.search(url):
                continue

            # This is a good record that we want to write
            writer.writerow([url, data[USER_AGENT]])

        print(' done!')


if __name__ == '__main__':
    main()
