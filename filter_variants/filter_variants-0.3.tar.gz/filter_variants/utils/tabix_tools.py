import logging
from subprocess import call

logger = logging.getLogger(__name__)

def bgzip_file(file_path):
    """Try to bgzip file"""
    
    command = [
            'bgzip',
            '-f',
            file_path,
            ]
    logger.info("Running bgzip with command: {0}".format(' '.join(command)))
    
    try:
        call(command)
    except OSError as e:
        raise e
    
    logger.info("File was bgzipped successfully")
    return

def index_file(file_path):
    """Try to index a file with tabix"""
    
    command = [
            'tabix',
            '-p',
            'vcf',
            file_path
            ]
    logger.info("Running tabix index with command: {0}".format(' '.join(command)))
    
    try:
        call(command)
    except OSError as e:
        raise e
    
    logger.info("File was indexed successfully")
    return
