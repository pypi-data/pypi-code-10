#!/usr/bin/env python3

import argparse
import logging
import sys

from cdis_pipe_utils import pipe_util

import fastqc

def main():
    parser = argparse.ArgumentParser('FastQC tool')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)
    
    # Required flags.
    parser.add_argument('--uuid',
                        required = True,
                        help = 'uuid string',
    )
    parser.add_argument('-f', '--fastq',
                        action='append',
                        required=True
    )

    # setup required parameters
    args = parser.parse_args()
    uuid = args.uuid
    fastq_list = args.fastq
    
    logger = pipe_util.setup_logging(tool_name, args, uuid)
    engine = pipe_util.setup_db(uuid)

    fastqc.fastqc(uuid, fastq_list, engine, logger)
    return


if __name__ == '__main__':
    main()
