import os

from cdis_pipe_utils import df_util
from cdis_pipe_utils import pipe_util
from cdis_pipe_utils import time_util

def splitbam(uuid, bam_path, engine, logger):
    step_dir = os.getcwd()
    if pipe_util.already_step(step_dir, 'splitbam', logger):
        logger.info('already completed step `splitbam` of: %s' % bam_path)
    else:
        logger.info('running step `bamtofastq` of %s: ' % bam_path)
        log_path = 'listFile.log'
        out_path = 'split'
        cmd = ['bam', 'splitBam', '--in', bam_path, '--out', out_path, '--log', log_path ]
        output = pipe_util.do_command(cmd, logger)
        df = time_util.store_time(uuid, cmd, output, logger)
        df['bam_path'] = bam_path
        unique_key_dict = {'uuid': uuid, 'bam_path': bam_path}
        table_name = 'time_mem_bamutil_splitbam'
        df_util.save_df_to_sqlalchemy(df, unique_key_dict, table_name, engine, logger)
        pipe_util.create_already_step(step_dir, 'splitbam', logger)
        logger.info('completed running step `splitbam` of: %s' % bam_path)
    return
