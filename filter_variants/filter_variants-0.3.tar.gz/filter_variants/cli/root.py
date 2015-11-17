#!/usr/bin/env python
# encoding: utf-8
"""
filter_variants.py

Command line tool for annotating vcf variants with frequencies and then filter them based on frequency.

Created by Måns Magnusson on 2015-09-09.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""

from __future__ import (print_function)

import sys
import logging
import itertools

import click
import tabix

from codecs import open

from vcftoolbox import (HeaderParser, add_vcf_info, 
print_headers, print_variant)

from extract_vcf import Plugin

from filter_variants import logger as root_logger
from filter_variants import (__version__, init_log, LEVELS,)
from filter_variants.utils import (get_frequency, get_tabix_handle)

@click.command()
@click.argument('variant_file',
                    nargs=1,
                    type=click.File('r'),
                    metavar='<vcf_file> or -'
)
@click.option('--thousand_g',
                    type=click.Path(exists=True), 
                    help="Specify the path to a bgzipped vcf file"\
                         " (with index) with 1000g variants"
)
@click.option('--exac',
                    type=click.Path(exists=True), 
                    help="Specify the path to a bgzipped vcf file"\
                         " (with index) with ExAC variants"
)
@click.option('-t', '--treshold',
                    default=0.05, 
                    help="""Treshold for filter variants. Default 0.05"""
)
@click.option('-a', '--annotate',
                    is_flag=True, 
                    help="""If the variants should be annotated"\
                         " with the frequency"""
)
@click.option('-k', '--keyword',
                    multiple=True,
                    help="If variants are already annotated this is the"\
                         " keyword to look for",
)
@click.option('-o', '--outfile', 
                    type=click.File('w'),
                    help="Specify the path to a file where results should"\
                         " be stored."
)
@click.option('-v', '--verbose', 
                count=True,
                default=0,
                help=u"Increase output verbosity. Can be used multiple times, eg. -vv"
)
@click.option('-l', '--logfile',
                    type=click.Path(exists=False),
                    help=u"Path to log file. If none logging is "\
                          "printed to stderr."
)
def cli(variant_file, thousand_g, exac, treshold, outfile, annotate, keyword,
        verbose, logfile):
    """
    Filter vcf variants based on their frequency.
    
    One can use different sources by addind --keyword multiple times.
    Variants and frequency sources should be splitted and normalized(with vt).
    """
    loglevel = LEVELS.get(min(verbose,2), "WARNING")
    init_log(root_logger, logfile, loglevel)
    
    logger = logging.getLogger(__name__)
    
    #For testing
    logger = logging.getLogger("filter_variants.cli.root")
    logger.info("Running filter_variants version {0}".format(__version__))

    logger.info("Initializing a Header Parser")
    head = HeaderParser()
    
    for line in variant_file:
        line = line.rstrip()
        if line.startswith('#'):
            if line.startswith('##'):
                head.parse_meta_data(line)
            else:
                head.parse_header_line(line)
        else:
            break
    
    if line:
        variant_file = itertools.chain([line], variant_file)
    
    
    if thousand_g:
        logger.info("Opening 1000G frequency file with tabix open")
        try:
            thousand_g_handle = get_tabix_handle(thousand_g)
        except OSError as e:
            logger.critical(e.message)
            logger.info("Exiting")
            sys.exit(1)
        logger.debug("1000G frequency file opened")
        if annotate:
            head.add_info(
                "1000GAF",
                "1",
                'Float',
                "Frequency in the 1000G database."
            )
    
    if exac:
        logger.info("Opening ExAC frequency file with tabix open")
        try:
            exac_handle = get_tabix_handle(exac)
        except OSError as e:
            logger.critical(e.message)
            logger.info("Exiting")
            sys.exit(1)
        
        logger.debug("ExAC frequency file opened")
        if annotate:
            head.add_info(
                "ExACAF",
                "1",
                'Float',
                "Frequency in the ExAC database."
            )
    plugins = []
    for key in keyword:
        if key not in head.info_dict:
            logger.error("{0} is not defined in vcf header.".format(key))
            logger.info("Exiting")
            sys.exit(1)
        plugins.append(Plugin(
            name=key,
            field='INFO',
            data_type='float', 
            separators=[','], 
            info_key=key, 
            record_rule='max',
        ))
    
    print_headers(head, outfile)

    for line in variant_file:
        max_freq = 0
        line = line.rstrip()
        variant_line = line.split('\t')
        chrom = variant_line[0].strip('chr')
        position = int(variant_line[1])
        ref = variant_line[3]
        alternative = variant_line[4]
        logger.debug("Checking variant {0}".format(
            '_'.join([chrom, str(position), ref, alternative])
        ))
        for plugin in plugins:
            logger.debug("Getting frequency for {0}".format(
                plugin.name))
            frequency = plugin.get_value(variant_line=line)
            logger.debug("Found frequency {0}".format(
                frequency))
            if frequency:
                if float(frequency) > max_freq:
                    logger.debug("Updating max freq")
                    max_freq = float(frequency)
        if thousand_g:
            logger.debug("Getting thousand g frequency")
            frequency = get_frequency(
                chrom = chrom,
                pos = position,
                alt = alternative,
                tabix_reader = thousand_g_handle
                )
            logger.debug("Found frequency {0}".format(
                frequency))
            
            if frequency:
                if annotate:
                    line = add_vcf_info(
                        keyword='1000GAF', 
                        variant_line=line, 
                        annotation=frequency
                    )
                if float(frequency) > max_freq:
                    logger.debug("Updating max freq")
                    max_freq = float(frequency)
        if exac:
            logger.debug("Getting ExAC frequency")
            frequency = get_frequency(
                chrom = chrom,
                pos = position,
                alt = alternative,
                tabix_reader = exac_handle
                )
            logger.debug("Found frequency {0}".format(
                frequency))
            if frequency:
                if annotate:
                    line = add_vcf_info(
                        keyword='ExACAF', 
                        variant_line=line, 
                        annotation=frequency
                    )
                if float(frequency) > max_freq:
                    logger.debug("Updating max freq")
                    max_freq = float(frequency)

        if max_freq < treshold:
            print_variant(line, outfile)
        else:
            logger.debug("Frequency {0} is higher than treshold"\
            " {1}. Skip printing variant".format(max_freq, treshold))
    

if __name__ == '__main__':
    cli()
