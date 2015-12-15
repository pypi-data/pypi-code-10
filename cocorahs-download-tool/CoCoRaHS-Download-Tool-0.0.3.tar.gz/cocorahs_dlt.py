#! python

# #####################################################################
# Copyright (c) 2015, NMSU Board of Regeants
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions 
# are met:
# 
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in 
#    the documentation and/or other materials provided with the 
#    distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED 
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY 
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
# #####################################################################

# Standard Library Imports
import argparse
import datetime
import json
import sys
import urllib2


# This module's version number
__version__ = '0.0.3'


# #####################################################################
# The following module attributes are considered "constants" and to be 
# used without modification.
# #####################################################################

# Base URLs for CoCoRaHS data download.
DATA_URL = 'http://data.cocorahs.org/cocorahs/export/exportreports.aspx'
STNS_URL = 'http://data.cocorahs.org/cocorahs/export/exportstations.aspx'

# Default location values for keyword arguments.
DEFAULT_COUNTRY = 'USA'
DEFAULT_STATE = 'NM'
DEFAULT_COUNTY = ''

# Default date values for keyword arguments.
DEFAULT_START_DATE = datetime.date.today() - datetime.timedelta(days = 5)
DEFAULT_END_DATE = datetime.date.today()

# Default output format values for keyword arguments.
DEFAULT_OUTPUT_FORMATS = ('CSV', 'XML', 'SHEF', 'SHEFSnow',)
DEFAULT_OUTPUT_FORMAT = 'CSV'


# #####################################################################
# The following module functions should be considered "private" to this 
# module and should never be called externally.
# #####################################################################

def _params_str(**kwargs):

    params_str = ''

    # The standard arguments that denote which stations to use for 
    # data retrieval.
    country = kwargs.get('country', DEFAULT_COUNTRY)
    state = kwargs.get('state', DEFAULT_STATE)
    county = kwargs.get('county', DEFAULT_COUNTY)

    # Begin to create the GET request string.  If the county code is 
    # not provided in the command line arguments, then the county 
    # string will be left off.
    params_str = '?Country=' + country + '&State=' + state

    if county != '':
        params_str += '&County=' + county

    return params_str


def _retrieve(url):

    try:

        response = urllib2.urlopen(url)
        output = response.read()

    except Exception as e:

        sys.stderr.write(str(e) + '\n')
        output = ''

    return output


def _valid_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


# #####################################################################
# The following module functions are "public" functions, provided for 
# use within this module and external use by another module or script.
# #####################################################################

def data(**kwargs):

    # Get the values of the keyword arguments to construct a GET params 
    # string for data retrieval
    output_format = kwargs.get('output_format', DEFAULT_OUTPUT_FORMAT)
    start_date = kwargs.get('start_date', DEFAULT_START_DATE)
    end_date = kwargs.get('end_date', DEFAULT_END_DATE)
    comments = kwargs.get('comments', False)
    times_in_gmt = kwargs.get('times_in_gmt', False)

    # Get the GET string with the common parameters.
    params = _params_str(**kwargs)

    # Comments are only allowed when requesting data be returned 
    # formatted as XML.  The function raises an Exception if XML is 
    # not requested and comments are requested.
    if (output_format != 'XML') and (comments is True):
        raise Exception('When requesting comments, format must be XML.')

    params += '&ReportType=Daily' + \
            '&ReportDateType=reportdate' + \
            '&dtf=3' + \
            '&Format=' + output_format + \
            '&StartDate=' + start_date.strftime('%m/%d/%Y') + \
            '&EndDate=' + end_date.strftime('%m/%d/%Y')

    if comments is True:
        params += '&ResponseFields=all'

    if times_in_gmt is True:
        params += '&TimesInGMT=True'

    url = DATA_URL + params
    output = _retrieve(url)

    return output


def stations(**kwargs):

    # Get the GET string with the common parameters.
    params = _params_str(**kwargs)

    # Construct the URL to request CoCoRaHS stations.
    url = STNS_URL + params

    # Retrieve the station data.
    output = _retrieve(url)

    return output


# #####################################################################
# The "main" section of this module.  Used if this module is run as a 
# standalone script.  Provides the command line argument definitions.
# #####################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = 'subcommand')
    dparser = subparsers.add_parser('data')
    sparser = subparsers.add_parser('stations')

    # The base parser arguments.
    parser.add_argument('--country', 
        type = str, 
        dest = 'country', 
        default = DEFAULT_COUNTRY, 
        help = 'Specify the country for the returned data.')
    parser.add_argument('--state', 
        type = str, 
        dest = 'state', 
        default = DEFAULT_STATE, 
        help = 'Specify the state for the returned data.')
    parser.add_argument('--county', 
        type = str, 
        dest = 'county', 
        default = DEFAULT_COUNTY, 
        help = 'Specify the county for the returned data.')

    # The sub-parser arguments for downloading data.
    dparser.add_argument('--start_date', 
        type = _valid_date, 
        dest = 'start_date', 
        default = str(DEFAULT_START_DATE), 
        help = 'A start date in the form yyyy-mm-dd')
    dparser.add_argument('--end_date', 
        type = _valid_date, 
        dest = 'end_date', 
        default = str(DEFAULT_END_DATE), 
        help = 'An end date in the form yyyy-mm-dd')
    dparser.add_argument('--format', 
        choices = DEFAULT_OUTPUT_FORMATS, 
        dest = 'output_format', 
        default = DEFAULT_OUTPUT_FORMAT, 
        help = 'The output format of the data.')
    dparser.add_argument('--comments', action = 'store_true', 
        help = 'Request comments be included in output (XML output only)')
    dparser.add_argument('--times_in_gmt', action = 'store_true', 
        help = 'Request all times be in GMT.')

    # Parse the command line arguments
    args = parser.parse_args()
    subcommand = args.subcommand

    # Determine which data request we are making.  The data request
    # requires several more parameters to be passed in the request.
    if subcommand == 'data':

        # Comments are only allowed when requesting data be returned 
        # formatted as XML.  The script exits with an error if XML is 
        # not requested and comments are requested.
        if (args.output_format != 'XML') and (args.comments is True):
            parser.error('When requesting comments, format must be XML.')

        # Call this module's data function, passing the command line 
        # arguments as keyword arguments.
        output = data(**vars(args))

    elif subcommand == 'stations':

        # Call this module's stations function, passing the command 
        # line arguments as keyword arguments.
        output = stations(**vars(args))

    else:
        output = ''

    # Write the output of the script to standard out.  
    sys.stdout.write(output + '\n')

    # Explicitely exit the script
    sys.exit(0)


