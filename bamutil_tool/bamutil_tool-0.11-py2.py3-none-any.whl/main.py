#!/usr/bin/env python3

import argparse
import logging
import sys

from cdis_pipe_utils import pipe_util

import tools.splitbam as splitbam
#import tools.polishbam as polishbam
#import tools.validate as validate
#import tools.stats as stats

def main():
    parser = argparse.ArgumentParser('bamutil docker tool')

    # Logging flags.
    parser.add_argument('-d', '--debug',
        action = 'store_const',
        const = logging.DEBUG,
        dest = 'level',
        help = 'Enable debug logging.',
    )
    parser.set_defaults(level = logging.INFO)
    
    # Required flags.
    parser.add_argument('--tool_name',
                        required = True,
                        help = 'bamutil tool'
    )
    parser.add_argument('--uuid',
                        required = True,
                        help = 'uuid string',
    )
    
    # Tool flags
    parser.add_argument('--bam_path',
                        required = False
    )

    # setup required parameters
    args = parser.parse_args()
    tool_name = args.tool_name
    uuid = args.uuid

    logger = pipe_util.setup_logging(tool_name, args, uuid)
    engine = pipe_util.setup_db(uuid)

    be_lenient = True
    
    if tool_name == 'splitbam':
        bam_path = pipe_util.get_param(args, 'bam_path')
        splitbam(uuid, bam_path, engine, logger)
    else:
        sys.exit('No recognized tool was selected')
        
    return


if __name__ == '__main__':
    main()
