__author__ = 'ismailkaboubi'
import logging
from random import choice


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    def __init__(self, ip):
        self.ip = ip


    def filter(self, record):
        record.ip = self.ip
        return True



class AdaptedLogger(object):
    """
     This is a new Logger that includes new formated data to the logs
     You need to specify :
        - project name
        - ip for the current server
    And Everything will be injected to the context filter of default logging library
    """
    def __init__(self, project, ip):
        self.project = project
        self.ip = ip
        self.context = ContextFilter(self.ip)
        self.levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
        self.format = "%(asctime)-1s %(name)-1s %(levelname)-1s %(ip)-1s %(message)s"

    def set_format(self, format):
        self.format = format

    def get_logger(self):
        logging.basicConfig(level=logging.DEBUG,
                            format=self.format)
        logger = logging.getLogger(self.project)
        logger.addFilter(self.context)
        return logger

    ## only for testing ##
    def test_logger(self):
        for x in range(10):
            lvl = choice(self.levels)
            lvlname = logging.getLevelName(lvl)
            logger = self.get_logger()
            logger.log(lvl, "A message at %s level with %d %s", lvlname, 2, "parameters")



#This is only for testing new logger
if __name__ == "__main__":
    adapted_log = AdaptedLogger("retail_crm_server", "127.0.0.1")
    #log.test_logger()
    logger = adapted_log.get_logger()
    logger.debug("Testing Debug Message")
    logger.info("Testing Info Message")
    logger.warn("Testing Warn Message")
    logger.error("Testing Error Message")


