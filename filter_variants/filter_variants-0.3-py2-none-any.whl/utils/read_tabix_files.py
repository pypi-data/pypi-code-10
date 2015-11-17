import logging
from tabix import TabixError

logger = logging.getLogger(__name__)

def get_frequency(chrom, pos, alt, tabix_reader):
    """Return the frequency found for this variant
    
    
        Args:
            chrom (str): The chromosome that the variant resides on
            pos (int): The startposition for the variant
            alt (str): The altrnative
            thousand_g_handle (TabixHandle): A pytabix file handle
        
        Returns:
            thousand_g_freq (float): The frequency found
    """
    logger.debug("Checking thousand genomes frequency for variant on chromosome"\
                 " {0}, position {1}, alternative {2}".format(chrom, pos, alt))
    
    try:
        for record in tabix_reader.query(chrom, pos-1, pos):
            logger.debug("Found record {0}".format(record))
            #We can get multiple rows so need to check each one
            #We also need to check each one of the alternatives per row
            for i,alternative in enumerate(record[4].split(',')):
                if alternative == alt:
                    logger.debug("{0} matches alt".format(alternative))
                    for info in record[7].split(';'):
                        info = info.split('=')
                        if info[0] == 'AF':
                            frequencies = info[-1].split(',')
                            logger.debug("Returning allele frequency {0}".format(frequencies[i]))
                            return frequencies[i]
    except TabixError as e:
        logger.warning("Chromosome {0} does not exist in frequency file.".format(chrom))
    
    logger.debug("No frequency found. Returning None")
    
    return None
