import os
import logging

import tabix

from filter_variants.warnings import (NotZippedError, NotIndexedError)
from . import bgzip_file, index_file

logger = logging.getLogger(__name__)

def get_tabix_handle(file_path):
    """Return a Tabix vcf handle
    
        Check if vcf file is bgzipped and tabix indexed properly.
        If not try to bgzip and or index the file.
        
        Args:
            file_path(str)
        
        Returns:
            file_handle(Tabix handle)
    """
    try:
        file_handle = open_tabix_file(file_path)
    except NotZippedError as e:
        logger.warning(e.message)
        logger.info("Trying to bgzip file {0}".format(file_path))
        try:
            bgzip_file(file_path)
            file_path += '.gz'
        except OSError as e:
            raise OSError("Bgzip does not seem to be installed on your"\
                            " system")
        try:
            logger.info("Trying to create index for file {0}".format(file_path))
            index_file(file_path)
        except OSError as e:
            logger.critical("Tabix does not seem to be installed on your"\
                            " system")
            logger.info("Please install tabix")
            logger.info("Exiting")
            sys.exit(1)
        file_handle = open_tabix_file(file_path)
    
    except NotIndexedError as e:
        logger.warning(e.message)
        logger.info("Trying to create index for file {0}".format(
            file_path))
        try:
            index_file(file_path)
        except OSError as e:
            raise OSError("tabix does not seem to be installed on your"\
                            " system")
        file_handle = open_tabix_file(file_path)
    
    return file_handle
    

def open_tabix_file(file_path):
    """docstring for open_tabix_file"""
    file_handle = tabix.open(file_path)
    try:
        file_handle.query('1', 1, 100)
    except tabix.TabixError as e:
        logger.warning("Something wrong with tabix file: {0}".format(
            file_path))
        
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension != '.gz':
            raise NotZippedError("File {0} does not seem to be bgzipped".format(
                file_path))
        else:
            raise NotIndexedError("File {0} does not seem to be tabix"\
                                  " indexed".format(file_path))
    return file_handle
    