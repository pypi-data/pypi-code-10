#!/usr/bin/env python3

import argparse
import logging
import sys

from cdis_pipe_utils import pipe_util

import tools.bamfixmateinformation as bamfixmateinformation
import tools.bamindex as bamindex
import tools.bammarkduplicates as bammarkduplicates
import tools.bammarkduplicates2 as bammarkduplicates2
import tools.bammdnm as bammdnm
import tools.bammerge as bammerge
import tools.bamsort as bamsort
import tools.bamtofastq as bamtofastq
import tools.bamvalidate as bamvalidate

def main():
    parser = argparse.ArgumentParser('biobambam docker tool')

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
                        help = 'biobambam tool'
    )
    parser.add_argument('--uuid',
                        required = True,
                        help = 'uuid string',
    )
    
    # Tool flags
    parser.add_argument('--bam_path',
                        required = False
    )
    parser.add_argument('--reference_fasta_path',
                        required = False
    )

    # setup required parameters
    args = parser.parse_args()
    tool_name = args.tool_name
    uuid = args.uuid

    logger = pipe_util.setup_logging(tool_name, args, uuid)
    engine = pipe_util.setup_db(uuid)

    be_lenient = True
    
    if tool_name == 'bamfixmateinformation':
        bam_path = pipe_util.get_param(args, 'bam_path')
        bamfixmateinformation(uuid, bam_path, engine, logger, be_lenient)
    elif tool_name == 'bamindex':
        bam_path = pipe_util.get_param(args, 'bam_path')
        bamindex(uuid, bam_path, engine, logger)
    elif tool_name == 'bammarkduplicates':
        bam_path = pipe_util.get_param(args, 'bam_path')
        bammarkduplicates(uuid, bam_path, engine, logger)
    elif tool_name == 'bammarkduplicates2':
        bam_path = pipe_util.get_param(args, 'bam_path')
        bammarkduplicates2(uuid, bam_path, engine, logger)
    elif tool_name == 'bammdnm':
        bam_path = pipe_util.get_param(args, 'bam_path')
        reference_fasta_path = pipe_util.get_param(args, 'reference_fasta_path')
        bammdnm(uuid, bam_path, reference_fasta_path, engine, logger)
    elif tool_name == 'bammerge':
        bam_path = pipe_util.get_param(args, 'bam_path')
        bammerge(uuid, bam_path, engine, logger)
    elif tool_name == 'bamsort':
        bam_path = pipe_util.get_param(args, 'bam_path')
        reference_fasta_path = pipe_util.get_param(args, 'reference_fasta_path')
        bamsort(uuid, bam_path, reference_fasta_path, engine, logger)
    elif tool_name == 'bamtofastq':
        bam_path = pipe_util.get_param(args, 'bam_path')
        bamtofastq(uuid, bam_path, engine, logger)
    elif tool_name == 'bamvalidate':
        bam_path = pipe_util.get_param(args, 'bam_path')
        bamvalidate(uuid, bam_path, engine, logger, be_lenient)
    else:
        sys.exit('No recognized tool was selected')
        
    return


if __name__ == '__main__':
    main()
