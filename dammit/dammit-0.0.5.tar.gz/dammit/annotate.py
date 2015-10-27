#!/usr/bin/env python
from __future__ import print_function

import logging
import os
from platform import system
import sys

from . import common
from .report import get_report_tasks
from .tasks import get_transcriptome_stats_task, \
                   get_busco_task, \
                   get_group_task, \
                   get_link_file_task, \
                   get_transdecoder_predict_task, \
                   get_transdecoder_orf_task, \
                   get_hmmscan_task, \
                   get_cmscan_task, \
                   get_lastal_task, \
                   get_crb_blast_task, \
                   get_sanitize_fasta_task

logger = logging.getLogger(__name__)

def get_tasks(transcriptome, database_dict, 
              n_threads=1, user_databases=[]):

    tasks = []
    results = {}

    tasks.append(
            get_sanitize_fasta_task(os.path.abspath(transcriptome),
                                    os.path.basename(transcriptome))
    )

    '''
    Calculate assembly information. First it runs some basic stats like N50 and
    number of contigs, and uses the HyperLogLog counter from khmer to
    estimate unique k-mers for checking redundancy. Then it runs BUSCO to
    assess completeness. These tasks are grouped under the 'assess' task.
    '''
    assess_tasks = []
    assess_tasks.append(
        get_transcriptome_stats_task(transcriptome, 
                                     os.path.basename(transcriptome + '.stats'))
    )
    results['stats'] = transcriptome + '.stats'

    '''
    BUSCO assesses completeness using a series of curated databases of core
    conserved genes.
    '''
    busco_cfg = common.CONFIG['settings']['busco']
    busco_output_name = '{0}.busco.results'.format(transcriptome)
    assess_tasks.append(
        get_busco_task(transcriptome, busco_output_name, database_dict['BUSCO'],
                       'trans', n_threads, busco_cfg)
    )
    results['busco'] = os.path.join('run_' + busco_output_name, 
                                    'short_summary_' + busco_output_name)

    # Collect the stats and BUSCO tasks under an "assess" group for convenience
    tasks.extend(assess_tasks)
    tasks.append(get_group_task('assess', assess_tasks))

    '''
    Run TransDecoder. TransDecoder first finds long ORFs with
    TransDecoder.LongOrfs, which are output as a FASTA file of protein
    sequences. We can then use these sequences to search against Pfam-A for
    conserved domains. TransDecoder.Predict uses the Pfam results to train its
    model for prediction of gene features.
    '''

    annotate_tasks = []

    transdecoder_output_dir = transcriptome + '.transdecoder_dir'
    orf_cfg = common.CONFIG['settings']['transdecoder']['longorfs']
    annotate_tasks.append(
        get_transdecoder_orf_task(transcriptome, 
                                  orf_cfg)
    )
    orf_pep = os.path.join(transdecoder_output_dir,
                               'longest_orfs.pep')
    orf_gff3 = os.path.join(transdecoder_output_dir,
                            'longest_orfs.gff3')
    results['ORFs_pep'] = orf_pep
    results['ORFs_gff3'] = orf_gff3

    pfam_results = transcriptome + '.pfam-A.tbl'
    annotate_tasks.append(
        get_hmmscan_task(orf_pep, pfam_results,
                     database_dict['PFAM'], n_threads, 
                     common.CONFIG['settings']['hmmer']['hmmscan'])
    )
    results['pfam'] = pfam_results

    predict_cfg = common.CONFIG['settings']['transdecoder']['predict']
    annotate_tasks.append(
        get_transdecoder_predict_task(transcriptome, 
                                      pfam_results,
                                      n_threads,
                                      predict_cfg)
    )
    protein_prediction_pep = transcriptome + '.transdecoder.pep'
    protein_prediction_gff3 = transcriptome + '.transdecoder.gff3'
    results['prot_predictions_pep'] = protein_prediction_pep
    results['prot_predictions_gff3'] = protein_prediction_gff3

    '''
    Run Infernal. Infernal uses covariance models to detect
    RNA secondary structures. Here we use Rfam as our reference
    database.
    '''
    cmscan_cfg = common.CONFIG['settings']['infernal']['cmscan']
    rfam_results = transcriptome + '.rfam.tbl'
    annotate_tasks.append(
        get_cmscan_task(transcriptome, rfam_results,
                     database_dict['RFAM'], n_threads, 
                     cmscan_cfg)
    )
    results['rfam'] = rfam_results

    '''
    Run LAST to get homologies with OrthoDB. We use LAST here because
    it is much faster than BLAST+, and OrthoDB is pretty huge.
    '''
    
    lastal_cfg = common.CONFIG['settings']['last']['lastal']
    orthodb_fn = database_dict['ORTHODB']
    tr_x_orthodb_fn = '{0}.x.orthodb.maf'.format(transcriptome)
    annotate_tasks.append(
        get_lastal_task(transcriptome, orthodb_fn, tr_x_orthodb_fn, True,
                       n_threads, lastal_cfg)
    )
    results['orthodb'] = tr_x_orthodb_fn
 

    '''
    Run conditional recipricol best hits blast (CRBB) against the
    user-supplied databases.
    '''
    results['user'] = {}
    crb_blast_cfg = common.CONFIG['settings']['crb-blast']
    for path in user_databases:
        key = os.path.basename(path)
        tasks.append(
            get_sanitize_fasta_task(os.path.abspath(path),
                                    key)
        )
        fn = '{0}.x.{1}.crbb.tsv'.format(transcriptome, key)
        annotate_tasks.append(
            get_crb_blast_task(transcriptome, key, fn, 
                               crb_blast_cfg, n_threads)
        )
        results['user'][key] = fn

    tasks.extend(annotate_tasks)

    outputs, report_tasks = get_report_tasks(transcriptome, results,
                                             database_dict,
                                             n_threads=n_threads)
    tasks.extend(report_tasks)

    return results, tasks

def get_doit_config(output_dir, transcriptome):

    doit_config = {
                    'reporter': common.LogReporter(logger),
                    'backend': common.DOIT_BACKEND,
                    'verbosity': common.DOIT_VERBOSITY,
                    'dep_file': os.path.join(output_dir, '.' +
                                             os.path.basename(transcriptome) +
                                             '.doit.db')
                  }
    return doit_config

def run_tasks(transcriptome, output_dir, tasks, args=['run']):
    '''
    Set up doit's config for the actual analysis tasks.
    We'll put the doit database for these tasks into the output
    directory so that we don't end up scattering them around the
    filesystem, or worse, with one master db containing dependency
    metadata from every analysis ever run by the user!
    '''

    doit_config = get_doit_config(output_dir, transcriptome)

    cwd = os.getcwd()
    logger.debug('cwd: {0}'.format(cwd))
    try:
        if not os.path.exists(output_dir):
            logger.debug('makedirs: {0}'.format(output_dir))
            os.makedirs(output_dir)
        os.chdir(output_dir)

        common.run_tasks(tasks, args, config=doit_config)
    finally:
        logger.debug('chdir: {0}'.format(cwd))
        os.chdir(cwd)

